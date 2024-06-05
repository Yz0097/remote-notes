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