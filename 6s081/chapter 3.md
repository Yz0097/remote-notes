#operating_system
# Translating
## several terms
### 1. PTE
- PTE(Page Table entity)
- 64 bits -> 1 PTE
```
63-54: Reserved
53-10: 44 bits PPN(Physical Page Number)
9 -0 : 10 bits falgs
```
- flags :
```
0: Valid
1: Readable
2: Writable
3: X - Executable
4: User
5: Global
6: Accessed
7: Dirty (0 in page directory)
8, 9: Reserved
```

### 2. Physical address
44 bits PPN + 12 bits offset    
PPN: from PTE in level 3 page table
offset : copied from VA, lowest 12bits

### 3. Virtual Address
11-0: offset
20-12: L0(9 bits)
21-13: L1
30-22: L2
`| L2 | L1 | L0 | OFFSET |`

## translating steps
3 steps for 3-level tree
nodes in tree: 4096 bytes Page Table, 512 PTEs. Need a 9 bits index for every page table.
1. use L2 to find the PTE in root page table, the PTE's PPN refer to a intermediate level page table;
2. use L1 to find the PTE in intermediate page table, and refers to the bottom level page table
3. L0 for bottom level page table, the specified PTE's 44 bits PPN for PA's top 44 bits, and cpoy 12 bits OFFSET from VA.
![[20240904170428.png]]

# kernel space
RAM中0x8000 0000(KERNBASE) 到 0x8640 0000(PHYSTOP)为内核地址空间。
这一部分的地址va=pa。
### 例外
也有部分内核地址va!=pa: trampoline page & kernel stack page
#### trampoline page
记录trampoline代码的物理页被映射了两次：1. va空间顶部；2. 直接映射
#### kernel stack page
每个进程拥有kernel stack，被设置在地址高处，地址低处有一个guard page， 未被映射（i.e. PTE_V为设置），这样stack泄露（overflow）时会进入panic。


## vm.c
### pagetable_t
```cpp
typedef uint64 *pagetable_t; // 512 PTEs
```
指向一个内核PTB，或者一个pre-进程PTB
### walk()
```cpp
//line 
pte_t *
walk(pagetable_t pagetable, uint64 va, int alloc)
{
  if(va >= MAXVA)
    panic("walk");

  for(int level = 2; level > 0; level--) {
    pte_t *pte = &pagetable[PX(level, va)];
    //PX用于取出L2，L1对应的9bits，对应PTB中PTE的编号
    if(*pte & PTE_V) {
    //#define PTE_V (1L << 0) 
    //1L表示64bits长整数，左移4位后进行与或运算，得到小头第五位的值
    //PTE中小头第五位即valid位
      pagetable = (pagetable_t)PTE2PA(*pte);
      //#define PTE2PA(pte) (((pte) >> 10) << 12)
      //PTE的小头前10位为flags，置0便于后序操作
    } else {
    //若指向valid位不为1的PTB，需要重新分配内存
      if(!alloc || (pagetable = (pde_t*)kalloc()) == 0)
        return 0;
      memset(pagetable, 0, PGSIZE);
      *pte = PA2PTE(pagetable) | PTE_V;
    }
  }
  return &pagetable[PX(0, va)];
}
```

### mappages()
给定一个页表、一个虚拟地址和物理地址，创建一个PTE以实现相应的映射
```cpp
//line 149
int
mappages(pagetable_t pagetable, uint64 va, uint64 size, uint64 pa, int perm)
{
  uint64 a, last;
  pte_t *pte;

  a = PGROUNDDOWN(va);
  last = PGROUNDDOWN(va + size - 1);
  //#define PGROUNDUP(sz)  (((sz)+PGSIZE-1) & ~(PGSIZE-1))
  //#define PGROUNDDOWN(a) (((a)) & ~(PGSIZE-1))
  for(;;){
    if((pte = walk(pagetable, a, 1)) == 0)
      return -1;
    if(*pte & PTE_V)
      panic("remap");
    *pte = PA2PTE(pa) | perm | PTE_V;
    if(a == last)
      break;
    a += PGSIZE;
    pa += PGSIZE;
  }
  return 0;
}
```
### satp & TLB
every CPU has its own satp, storing the bottom physical address of the root page table.
TLB (Translation Look-aside Buffer): cach some PTEs for translation

### 