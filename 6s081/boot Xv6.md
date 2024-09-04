#operating_system
# xv6的启动过程
相关代码: entry.S start.c main.c
## kernel/entry.S
- machine mode
首先qemu中,将xv6加载到物理内存. pc指针(寄存器)指向0x8000 0000, 即entry.S开始的位置. entry.S设置sp(栈寄存器), 这样系统得以运行C代码, 进入start.c中,执行start()函数

## kernel/start.c
- machine mode -> supervisor mode
start在机器态下设置 
	*1* 特权寄存器 
	*2* 时钟中断 
	*3* 将CPU id放入reg tp中,每一个CPU需要对应的位置
初始化设置完成后, 进入内核态(supervisor/kernel mode), 使用mret指令(start.c line 49)

## kernel/main.c
- supervisor mode -> user mode
### userinit()函数
函数定义在proc.c中,初始化了第一个用户进程. 执行initcode(一段汇编代码)如下:
```ASM
auipc  a0, 0
addi   a0, a0, 36  # a0 = 36 = "\init\0"
auipc  a1, 0
addi   a1, a1, 35  # a1 = 43 = &NULL
add    a7, x0, 7
ecall              # exec init
add    a7, x0, 2
ecall              # exec exit
jal    ra, -8      # exit
```


```C
uchar initcode[] = {
  0x17, 0x05, 0x00, 0x00, 0x13, 0x05, 0x45, 0x02,
  0x97, 0x05, 0x00, 0x00, 0x93, 0x85, 0x35, 0x02,
  0x93, 0x08, 0x70, 0x00, 0x73, 0x00, 0x00, 0x00,
  0x93, 0x08, 0x20, 0x00, 0x73, 0x00, 0x00, 0x00,
  0xef, 0xf0, 0x9f, 0xff, 0x2f, 0x69, 0x6e, 0x69,
  0x74, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00
};
```

### void scheduler(void)
init: *1* fork+exec sh *2* wait(0) 清理僵尸进程
sh: 控制台程序

![[syscall.png]]
![[usermode.png]]
![[supervisorreg.png]]
![[commonreg.png]]
