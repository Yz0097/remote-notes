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


