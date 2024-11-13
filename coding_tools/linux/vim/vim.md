#coding #vim
## insert
### 进入insert模式
1. i insert
2. A append at end of line
# normal
1. : 后接指令
2. y yawn 复制；p paste
3. u undo
4. \<num> + hjkl 跳转num行/列
5. v 开始多选

# bug
vmware中进入vim界面之后，`a`进入输入模式，此时按上下左右键会变成输入ABCD，backspace键按下后会退出输入模式
https://blog.csdn.net/sinat_27180563/article/details/81609655
apt-get remove vim-common，然后重新安装vim