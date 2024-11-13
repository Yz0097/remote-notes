#coding #operating_system 
# 压缩
tar指令压缩文件夹
`tar -czvf archive-name.tar.gz /path/to/directory`

压缩文件
`tar -zxvf name.tar.gz /path/to/file`

# 解压
在‌Linux系统中，可以使用tar命令来解压tar文件。基本命令格式如下：
`tar -xvf 文件名.tar`
其中，-x表示解压文件，-v表示显示详细信息，-f表示指定要解压的文件。
### 解压到指定目录
如果希望将tar文件解压到指定的目录，可以使用-C选项：
`tar -xvf 文件名.tar -C 目标目录`

### 解压压缩过的tar文件
如果tar文件是压缩过的（如.tar.gz、.tar.bz2等），需要使用相应的解压命令或工具进行解压：#
对于**gzip**压缩的tar文件：
`tar -xzvf 文件名.tar.gz`
对于**bzip2**压缩的tar文件：
`tar -xjvf 文件名.tar.bz2`