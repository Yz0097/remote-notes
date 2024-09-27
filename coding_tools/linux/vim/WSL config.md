
#operating_system #coding
# ubuntu 20.04
安装wsl的主要目的是寻找一个更高效的文本处理方式，我尝试使用[[vim]]来提高自己的效率，同时也试着配置一系列相应的环境来配合vim编辑器。譬如我希望能做到屏幕上在使用vim编辑md的同时可以预览到渲染后的md文件，也希望能够在md中插入本地文件。  
通过bilibili上TheCW大佬的教学，我希望在linux上自定义一个合适的工作环境，但是碍于硬件受限，最初我选择了WSL系统。经过几天与WSL系统的鏖战，似乎仍然没有一个比较好的效果。意料之外的找到了obsidian软件，除了在vim中没有一个足够强大的命令行指令之外，这款软件在笔记和markdown上的表现令我十分满意（但是在笔记的整体过程中无法达到完全脱离鼠标的目的）。
## win10家庭中文版安装wsl以及ubuntu发行版

1. 安装hyper-v并启动
2. 运行如下bat脚本（管理员）
```cmd_script{.line-numbers}
pushd "%~dp0"
dir /b %SystemRoot%\servicing\Packages\*Hyper-V*.mum >hyper-v.txt
for /f %%i in ('findstr /i . hyper-v.txt 2^>nul') do dism /online /norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"
del hyper-v.txt
Dism /online /enable-feature /featurename:Microsoft-Hyper-V-All /LimitAccess /ALL
```
此时报错0x800701bc，需要安装wsl-update-x64  
msi安装过程中报错2503，2502  
cmd(管理员)msiexec /package \<MSI FILE NAME>  
此时安装成功，可以安装ubuntu20.04，退出关闭wsl分发版后再次开启，报错0x80072ee2  
代理软件的问题，在启动前使用指令`netsh winsock reset `
重启电脑后发现问题解决，不需要重置winsock目录，ubuntu20.04中也可以ping通百度　
_大约三天之后又遇到这个问题 通过`net winsock reset`解决了  
参考：http://www.taodudu.cc/news/show-5825861.html?action=onClick  

## 安装ranger
_后改为使用joshuto_  `apt-get -install ranger`

## 安装并配置xrdp

```shell
$ sudo apt install xrdp -y #安装xrdp
$ sudo cp /etc/xrdp/xrdp.ini /etc/xrdp/xrdp.ini.backup #备份
$ sudo vim /etc/xrdp/xrdp.ini #将3389端口改为3390端口(如下图)
$ sudo service xrdp start #打开xrdp
```

windows中运行mstsc.exe，链接到localhost:3390, 可以打开远程桌面，运行i3wm桌面  
--https://zhuanlan.zhihu.com/p/567827887

## 配置wsl内存限制
c\users\hp\.wslconfig
内容如下：
```
[wsl2]
processors=8\限制核心数量
memory=2GB\限制内存
swap=<size> \限制交换分区
localhostForwarding=true\关闭默认连接，将WSL2本地主机绑定到Windows本地主机
```
--https://www.cnblogs.com/yyfh/p/16526955.html

## 安装git
apt install git build-essential cargo

# 常用的WSL以及shell指令
1. `wsl -l -v`  
	可以查看已经安装的发行版及其状态
2. `wsl -d <发行版名字>`  
	可以启动对应的发行版
3. `wsl -t <发行版名字>`  
	关闭发行版，相当于在终端下使用`sudo shutdown now`指令

# 终端与shell
## 终端模拟器
alacritty
## 窗口管理器
gui like gnome(or these gui interface include a window manager) \ flat windows manager like i3wm, dwm
## shell
使用bash或者zsh windows中使用conhost(cmd)\powershell