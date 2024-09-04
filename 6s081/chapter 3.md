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

## details
### walk

### satp & TLB
every CPU has its own satp, store the bottom physical address of the root page table.
TLB (Translation Look-aside Buffer): cach some PTEs for translation

### 