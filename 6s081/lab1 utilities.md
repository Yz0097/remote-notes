#operating_system
# 1 boot xv6
```shell
git clone git://g.csail.mit.edu/xv6-labs-2020
```
vmware虚拟机无法连接（没有vpn），选择直接在本地git init了一个git仓库。
课程提供的仓库有master和util两个branch。相关操作：
- git branch <branch_name> //查询仓库分支; 创建新的分支
- git checkout <branch_name> //切换当前分支

进入xv6操作系统: 在xv6-labs-2020仓库下
```shell
make qemu
```
退出xv6: ctrl-a x. 

# 2 sleep


```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main(int argc, char *argv[])
{
    // no param
    if (argc <= 1)
    {
        fprintf(2, "sleep: error no argument\n");
        exit(1);
    }

    //sleep
    int sleep_time = atoi(*argv);
    sleep(sleep_time);
    
    exit(0);
}
```
points: 
1. 处理没有输入参数的情况, 返回错误信息
2. atoi的使用, 在user/ulib.c中有实现, 一般的在头文件stdlib.h中也有

在Makefile中添加, 将sleep加入shell指令中:
```Makefile
UPROGS=\
	... ... ...
	$U/_sleep\
```

# 3 pingpong
file descriptor 
- fd0: standard input
- fd1: standard output
- fd2: standard error

使用两个pipe, 分别用于parent->child和child->parent的传输.

```C
#define WRITE 1
#define READ 0
#define ERROR 2
int main(void)
{
    
    int p1[2]; // child -> parent
    int p2[2]; // parent -> child
    pipe(p1);
    pipe(p2);
    int pid = fork();

    if (pid == 0)
    { // child
        char child_buffer[10] = "ping";
        char recieve_buffer[10];

        close(p1[WRITE]);
        close(p2[READ]);

        read(p2[READ], recieve_buffer, 10);
        fprintf(0, "%d: received %s\n", getpid(), recieve_buffer);
        write(p1[WRITE], child_buffer, 10);

        close(p1[READ]);
        close(p2[WRITE]);
    }
    else if (pid > 0)
    { // parent
        char parent_buffer[10] = "pong";
        char recieve_buffer[10];

        close(p1[READ]);
        close(p2[WRITE]);

        read(p1[READ], recieve_buffer, 10);
        fprintf(0, "%d: received %s\n", pid, recieve_buffer);
        write(p2[WRITE], parent_buffer, 10);

        close(p1[WRITE]);
        close(p2[READ]);
    }
    else
    { // error
        fprintf(2, "Error: pipe error.\n");
    }

    exit(0);
}
```

出现如下情况:
```shell
$ pingpong
3: received pong
4: rece$ ived ping
```
是由于子进程没有结束输出, 父进程就退出导致的. 在父进程的最后添加
```C
wait((int*) 0);
```
等待子进程执行结束后再退出

# 4 primes

```C
void child(int *pl){
    int n;
    
    close(pl[WRITEEND]);////important
    //without this sentence, only prime 13
    int if_read = read(pl[READEND], &n, sizeof(int));
    if(if_read == 0){
        exit(0);
    }

    int pr[2];
    pipe(pr);
    int pid = fork();

    if(pid == 0){
        //child
        child(pr);
    }else{
        //parent
        close(pr[READEND]);
        printf("prime %d\n", n);
        //close(p[WRITEEND]);
        
        int prime=n;
        while(read(pl[READEND], &n, sizeof(int)) != 0){
            if(n%prime != 0){
                write(pr[WRITEEND], &n, sizeof(int));
            }
        }
        close(pr[WRITEEND]);
        wait((int*) 0);
        exit(0);
    }
}


int main(void){
    int p[2];
    pipe(p);
    int pid = fork();

    if(pid == 0){
        //child
        child(p);
    }else{
        //parent
        close(p[READEND]);
        for(int i = 2; i < 36; i++){
            write(p[WRITEEND], &i, sizeof(int));
        }
        close(p[WRITEEND]);
        wait((int*) 0);
    }
    exit(0);
}
```

每次递归以第一个读入的数(最小数)作为素数, 不能被这个数整除的传入下一轮递归.
如果在递归函数开头不关闭左侧管道的readend,递归会无法继续进行, 卡在prime 13 的位置[TODO]

# find 
ls.c[https://zhuanlan.zhihu.com/p/669012113]
