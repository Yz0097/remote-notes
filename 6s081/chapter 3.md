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
//return addr of PTE in the lowest layer of PTB tree
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


### satp & TLB
every CPU has its own satp, storing the bottom physical address of the root page table.
TLB (Translation Look-aside Buffer): cach some PTEs for translation

# 初始化页表
参考[[boot Xv6#kvminit()]]中. 
`kvminit()`函数调用`kvmmake()` 来初始化一个内核页表, 在新版代码中已经删除.
`kvminit`直接使用`memset`, `kvmmap`来初始化.
此时的地址直接指向pa.
随后会调用`kvminithart`来将页表装入satp寄存器中.
### kvminit()
```cpp
void
kvminit()
{
  kernel_pagetable = (pagetable_t) kalloc();
  memset(kernel_pagetable, 0, PGSIZE);

  // uart registers
  kvmmap(UART0, UART0, PGSIZE, PTE_R | PTE_W);

  // virtio mmio disk interface
  kvmmap(VIRTIO0, VIRTIO0, PGSIZE, PTE_R | PTE_W);

  // CLINT
  kvmmap(CLINT, CLINT, 0x10000, PTE_R | PTE_W);

  // PLIC
  kvmmap(PLIC, PLIC, 0x400000, PTE_R | PTE_W);

  // map kernel text executable and read-only.
  kvmmap(KERNBASE, KERNBASE, (uint64)etext-KERNBASE, PTE_R | PTE_X);

  // map kernel data and the physical RAM we'll make use of.
  kvmmap((uint64)etext, (uint64)etext, PHYSTOP-(uint64)etext, PTE_R | PTE_W);

  // map the trampoline for trap entry/exit to
  // the highest virtual address in the kernel.
  kvmmap(TRAMPOLINE, (uint64)trampoline, PGSIZE, PTE_R | PTE_X);
}

// Switch h/w page table register to the kernel's page table,
// and enable paging.
void
kvminithart()
{
  w_satp(MAKE_SATP(kernel_pagetable));
  sfence_vma();
}
```

### kvmmap()
```cpp
// add a mapping to the kernel page table.
// only used when booting.
// does not flush TLB or enable paging.
void
kvmmap(uint64 va, uint64 pa, uint64 sz, int perm)
{
  if(mappages(kernel_pagetable, va, sz, pa, perm) != 0)
    panic("kvmmap");
}
```

### mappages()
给定一个页表、一个虚拟地址和物理地址，创建一个PTE以实现相应的映射
```cpp
//line 149
int
mappages(pagetable_t pagetable, uint64 va, uint64 size, uint64 pa, int perm)
{
//return 0 -> success; panic remap:pte not valid ; 
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

### Proc_mapstacks
现为procinit(), 为每个进程分配一个kernel stack
```cpp
void
procinit(void)
{
  struct proc *p;
  
  initlock(&pid_lock, "nextpid");
  for(p = proc; p < &proc[NPROC]; p++) {
      initlock(&p->lock, "proc");

      // Allocate a page for the process's kernel stack.
      // Map it high in memory, followed by an invalid
      // guard page.
      char *pa = kalloc();
      if(pa == 0)
        panic("kalloc");
      uint64 va = KSTACK((int) (p - proc));
      kvmmap(va, (uint64)pa, PGSIZE, PTE_R | PTE_W);
      p->kstack = va;
  }
  kvminithart();
}
```

## TLB快表
TLB, Translation Look-aside Buffer.
`sfence.vma`:flush当前CPU的TLB. 当xv6修改PTB的时候, 必须同时修改TLB中对应的项目. 更简单的方法是直接清空.
可以看到当`kvminithart`重载satp寄存器后, 需要调用`sfence.vma`来清空TLB.[[chapter 3#kvminit()]]

## allocate
xv6维护一个记录空闲区域的链表.分配时从链表中移除, 释放时加入链表. 每次分配释放都以4096 bytes为单位.

## kalloc.c
kmem是一个链表, 包含一个spinlock, 和一个指向`run`的指针. run是链表中记录空闲地址的结点. 

# 3.6 进程地址空间

>Each process has a separate page table, and when xv6 switches between processes, it also changes page tables. As Figure 2.3 shows, a process’s user memory starts at virtual address zero and can grow up to MAXVA (kernel/riscv.h:360), allowing a process to address in principle 256 Gigabytes of memory.

每个进程拥有一张独立的页表, 当xv6在进程间切换时, 同时也会切换页表. 如图2.3, 一个进程的用户内存从虚拟地址0开始, 最多可以增长到`MAXVA`(kernel/riscv.h:360), 原则上允许一个进程最多占用256GB的内存.
>When a process asks xv6 for more user memory, xv6 first uses kalloc to allocate physical pages. It then adds PTEs to the process’s page table that point to the new physical pages. Xv6 sets the PTE_W, PTE_X, PTE_R, PTE_U, and PTE_V flags in these PTEs. Most processes do not use the entire user address space; xv6 leaves PTE_V clear in unused PTEs.

当一个进程向xv6请求更多的用户内存时, xv6首先使用`kalloc`来分配物理页. 随后它会将得到的PTEs添加到进程的页表中, 指向新的物理页. Xv6设置这些PTE的WXRUV标志位.大部分经常不会完整的使用用户地址空间. xv6会保持未使用的PTE的标志位V为0.

>We see here a few nice examples of use of page tables. First, different processes’ page tables translate user addresses to different pages of physical memory, so that each process has private user memory. Second, each process sees its memory as having contiguous virtual addresses starting at zero, while the process’s physical memory can be non-contiguous. Third, the kernel maps a page with trampoline code at the top of the user address space, thus a single page of physical memory shows up in all address spaces.

