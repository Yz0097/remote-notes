# 1 trace
## 如何创建一个系统调用
[[https://zhuanlan.zhihu.com/p/668632093]]
[[https://fanxiao.tech/posts/2021-03-02-mit-6s081-notes/#25-lab-2-system-calls]]
以创建trace为例
### 1 
创建`kernel/sys_trace.c` 
注意，这里的 .c 文件只是起一个归纳作用，而不是像用户态那样一个文件一个命令。比如，所有和进程相关的系统调用都在 `kernel/sysproc.c` 中实现。    
用户态命令需要 main 函数作为入口，因此一个文件对应一个命令，而内核系统调用则不需要如此。
### 2
`kernel/syscall.h`中添加系统调用编号
```C
// System call numbers
#define SYS_fork    1
#define SYS_exit    2
// ... ...
#define SYS_close  21
#define SYS_trace  22
```
然后，在 `kernel/syscall.c` 中用 extern 全局声明新的内核调用函数，并且在 syscalls 映射表中，加入从前面定义的编号到系统调用函数指针的函数。
```C
extern uint64 sys_chdir(void);
extern uint64 sys_close(void);
//... ...
extern uint64 sys_uptime(void);
extern uint64 sys_trace(void);

static uint64 (*syscalls[])(void) = {
[SYS_fork]    sys_fork,
[SYS_exit]    sys_exit,
//... ...
[SYS_close]   sys_close,
[SYS_trace]  sys_trace,
};
```

### 3
在 `user/usys.pl` 中，加入用户态到内核态的跳板函数
```C
entry("fork");
entry("exit");
//... ...
entry("trace");
```
这个脚本在 make qemu 后会生成 usys.S 汇编文件，里面定义了每个系统调用的用户态跳板函数, 如:
```ASM
trace:
 li a7, SYS_trace
 ecall
 ret
```

### 4
用户态的头文件`user/user.h`中加入定义，使得用户态程序可以找到这个跳板的入口。

```C
// system calls
int fork(void);
int exit(int) __attribute__((noreturn));
//... ...
int trace(int);
```

如此繁琐的操作，就是为了实现内核态与用户态的隔离，保证安全。而这样就引出了一个问题，系统调用的参数怎么传递？

由于内核与用户进程的页表不同，寄存器也不互通，所以参数无法直接通过 C 语言参数的形式传过来，而是需要使用 argaddr、argint、argstr 等系列函数，从进程的 trapframe 中读取用户进程寄存器中的参数。

同样的，页表不同，指针也不同，内核不能直接对用户态传进来的指针进行解引用，而是需要使用 copyin、copyout 方法结合进程的页表，才能顺利找到用户态指针（逻辑地址）对应的物理内存地址。因此，当系统调用传递给用户态返回值时，则需要通过 copyout 来拷贝。

一个系统调用执行的过程如下:

| 文件名              | 作用                                                     |
| ---------------- | ------------------------------------------------------ |
| user/user.h      | 用户态程序调用跳板函数                                            |
| user/usys.S      | 跳板函数使用 CPU 提供的 ecall 指令，调用到内核态                         |
| kernel/syscall.c | 到达内核态统一系统调用处理函数 syscall()，所有系统调用都会跳到这里来处理。             |
| kernel/syscall.c | syscall() 根据跳板传进来的系统调用编号，查询 syscalls[] 表，找到对应的内核函数并调用。 |
| kernel/sysproc.c | 到达 sys_xxx() 系统调用函数，执行具体内核操作                           |

## lab: system call tracing

	In this assignment you will add a system call tracing feature that may help you when debugging later labs. You'll create a new trace system call that will control tracing. It should take one argument, an integer "mask", whose bits specify which system calls to trace. For example, to trace the fork system call, a program calls trace(1 << SYS_fork), where SYS_fork is a syscall number from kernel/syscall.h. You have to modify the xv6 kernel to print out a line when each system call is about to return, if the system call's number is set in the mask. The line should contain the process id, the name of the system call and the return value; you don't need to print the system call arguments. The trace system call should enable tracing for the process that calls it and any children that it subsequently forks, but should not affect other processes.

### 1 
struct proc结构体中添加一个新的变量trace_mask, 传递trace接受的mask值,首先在结构体定义处添加:
```C
//kernel/proc.h
struct proc {
  //... ...
  int trace_mask;              // Tracing mask
};

```

创建进程会调用 allocproc 函数来进行，因此需要在其中对 trace_mask 进行初始化。

```C
//kernel/proc.c line 92
static struct proc*
allocproc(void)
{
  // ... ... 

  //lab2
  p->trace_mask = 0;

  return p;
}
```

在fork函数中,子进程继承父进程的mask,保持对子进程的追踪
```C
//kernel/proc.c line 261
int
fork(void)
{
  int i, pid;
  struct proc *np;//child proc
  struct proc *p = myproc();
  // lab2: system call tracin
  //put line 270 right here: np uninitialized
  np->trace_mask = p->trace_mask;
  // ... ...
  return pid;
}
```

### 2
`kernel/sysproc.c`中, 加入sys_trace函数, 给trace_mask赋值
```C
uint64
sys_trace(void){
  int mask;
  argint(0,&mask);
  if(mask < 0){
    return -1;
  }
  struct proc *p = myproc();
  p->trace_mask = mask;
  return 0;
}
```
进行系统调用时, syscall函数中会读取reg a7的编号, 执行对应的系统调用, 原实现如下:
```C
void
syscall(void)
{
  int num;
  struct proc *p = myproc();

  num = p->trapframe->a7;
  if(num > 0 && num < NELEM(syscalls) && syscalls[num]) {
    p->trapframe->a0 = syscalls[num]();
  } else {
    printf("%d %s: unknown sys call %d\n",
            p->pid, p->name, num);
    p->trapframe->a0 = -1;
  }
}
```
只需在调用之前读取num, 打印输出对应的系统调用名称即可实现trace的输出:
```C
void
syscall(void)
{
  int num;
  struct proc *p = myproc();
  char* syscall_names[22] = {"fork", "exit", "wait", "pipe", "read", "kill", "exec", "fstat", "chdir", "dup", "getpid", "sbrk", "sleep", "uptime", "open", "write", "mknod", "unlink", "link", "mkdir", "close", "trace"};

  num = p->trapframe->a7;
  if(num > 0 && num < NELEM(syscalls) && syscalls[num]) {
    // Use num to lookup the system call function for num, call it,
    // and store its return value in p->trapframe->a0
    p->trapframe->a0 = syscalls[num]();
    // sys_trace插桩
    if((p->trace_mask >> num) & 1){
      printf("%d: syscall %s -> %d\n",p->pid, syscall_names[num-1], p->trapframe->a0);
    }
  } else {
    printf("%d %s: unknown sys call %d\n",
            p->pid, p->name, num);
    p->trapframe->a0 = -1;
  }
}
```

实现用户态的trace命令, 还需要编写`user/trace.c`, 并注册`UPROGS=\`    
实验中已经完成了这两步骤. 

# 2 sysinfo
	In this assignment you will add a system call, sysinfo, that collects information about the running system. The system call takes one argument: a pointer to a struct sysinfo (see kernel/sysinfo.h). The kernel should fill out the fields of this struct: the freemem field should be set to the number of bytes of free memory, and the nproc field should be set to the number of processes whose state is not UNUSED. We provide a test program sysinfotest; you pass this assignment if it prints "sysinfotest: OK".

## 1 准备工作
为了完成sysinfo的系统调用, 需要实现两个功能: 
1. 获取空闲内存大小`freemem`
2. 获取空闲进程数量`nproc`

### 1 获取空闲内存
参考`kernel/kalloc.c`中的写法. xv6 通过一个链表将各个空闲内存页连接起来，一个节点代表一个空闲内存页，形成一个空闲链表 freelist. 取用时使用根节点, 释放时插入到链表头部. 
```C
//kernel/kalloc.c line 21
struct {
  struct spinlock lock;
  struct run *freelist;
} kmem;
```
`kmem`是用于保存freepage的结构体. 在`kalloc.c`中添加如下函数:
```C
uint64
kcollect_free(void)
{
  acquire(&kmem.lock);

  uint64 free_bytes = 0;
  struct run *r = kmem.freelist;
  while(r){
    free_bytes += PGSIZE;
    r = r->next;
  }

  release(&kmem.lock);
  return free_bytes;
}
```

### 2 获取进程数
`kernel/proc.c`中使用`struct proc proc[NPROC]`保存所有进程. `proc.state==UNUSED`表示进程空闲. 
```C
// kernel/proc.c
int
collect_proc_num(void)
{
  int num = 0;
  struct proc *p;
  for(p = proc; p < &proc[NPROC]; p++){
    if(p->state != UNUSED)
      num++;
  }
  return num;
}
```

在`kernel/defs.h`中,需要添加这两个函数的声明,才能在编译时检测到这两个函数.

## 2 添加系统调用
在`kernel/sysproc.c`中添加
```C
uint64
sys_sysinfo(void)
{
    struct proc *p = myproc();

    struct sysinfo si;
    uint64 info_addr; // user pointer to struct stat
    if(argaddr(0, &info_addr) < 0)
      return -1;

    si.freemem = kcollect_free();
    si.nproc = collect_proc_num();

    // 将struct sysinfo拷贝至用户态
    if(copyout(p->pagetable, info_addr, (char*)&si, sizeof(si)) < 0){
        return -1;
    }
    return 0;
}
```