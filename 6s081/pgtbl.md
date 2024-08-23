# 1. kernel/vm.c
- vm: virtual memory
- kvm: kernel ~
- uvm: user ~
注意:kvm和uvm都运行在内核态中
## 1.1 全局变量
```C
/*
 * the kernel's page table.
 */
pagetable_t kernel_pagetable;

extern char etext[];  // kernel.ld sets this to end of kernel code.

extern char trampoline[]; // trampoline.S
```
### 1.1.1 pagetable_t
在riscv.h中定义了
```C
typedef uint64 pte_t;
typedef uint64 *pagetable_t; // 512 PTEs
```
一张pgtbl包含512条pte, 每个pte长度为64位, 对应uint64. (pte: page table entry)
MMU是CPU中的memory management unit, 访问虚拟地址时, MMU会将va翻译为对应的pa,pa被存储在reg satp中. 
### 1.1.2 etext[]
kernel.ld中:
```Linker
# kernel/kernel.ld (12-20行)
# 链接脚本中.的含义是当前地址计数器，可以直接引用当前地址位置
.text : {
    *(.text .text.*)		# 将所有文件的text text.*全部放置在kernel的代码段
    . = ALIGN(0x1000);		# 对齐至0x1000(4096)，即新开一个页面
    _trampoline = .;		# trampoline放置在下一个页的开头位置
    *(trampsec)				# 放置trampsec段到此处，trampsec段就是trampoline开头声明的
    . = ALIGN(0x1000);		# 再新开一个页面
    ASSERT(. - _trampoline == 0x1000, "error: trampoline larger than one page");
    PROVIDE(etext = .);		# 定义一个全局标号etext，等于此处地址.
  }
```
etext是一个指针，指向了kernel代码段最后的位置。
### 1.1.3 trampoline
指向trampoline.S的开头

## 1.2 walk
xv6 kernel va与pa之间是直接映射关系, 在这一前提下, walk才能够运行.
```C
// vm.c line 59
// Return the address of the PTE in page table pagetable
// that corresponds to virtual address va.  If alloc!=0,
// create any required page-table pages.
//
// The risc-v Sv39 scheme has three levels of page-table
// pages. A page-table page contains 512 64-bit PTEs.
// A 64-bit virtual address is split into five fields:
//   39..63 -- must be zero.
//   30..38 -- 9 bits of level-2 index.
//   21..29 -- 9 bits of level-1 index.
//   12..20 -- 9 bits of level-0 index.
//    0..11 -- 12 bits of byte offset within the page.
pte_t *
walk(pagetable_t pagetable, uint64 va, int alloc)
{
  if(va >= MAXVA)//va超出最大值
    panic("walk");
  
  for(int level = 2; level > 0; level--) {//xv6三级页表,查询两次
    pte_t *pte = &pagetable[PX(level, va)];//找到对应索引项
    if(*pte & PTE_V) {//判断pte_valid位
      pagetable = (pagetable_t)PTE2PA(*pte);
    } else {//根据alloc参数决定报错或者申请新的页表
      if(!alloc || (pagetable = (pde_t*)kalloc()) == 0)//或者无法分配新的页表
        return 0;//2,3级页表不存在且不需要分配时返回0
      memset(pagetable, 0, PGSIZE);
      *pte = PA2PTE(pagetable) | PTE_V;
    }
  }
  return &pagetable[PX(0, va)];
}
```
宏`PX(level,va)`从va中提取出level对应的9 bits索引. $2^9 = 512$, 一级页表中有512个pte
```C
// extract the three 9-bit page table indices from a virtual address.
#define PXMASK          0x1FF // 9 bits
#define PXSHIFT(level)  (PGSHIFT+(9*(level)))
#define PX(level, va) ((((uint64) (va)) >> PXSHIFT(level)) & PXMASK)
```

```C
// shift a physical address to the right place for a PTE.
#define PA2PTE(pa) ((((uint64)pa) >> 12) << 10)
#define PTE2PA(pte) (((pte) >> 10) << 12)
```