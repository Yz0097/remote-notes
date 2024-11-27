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

# 分屏
==‌**在[Vim](https://www.baidu.com/s?rsv_idx=1&wd=Vim&fenlei=256&usm=1&ie=utf-8&rsv_pq=bf5fb5aa00196ab7&oq=vim%20%E5%88%86%E5%B1%8F&rsv_t=154aV54dDwgXsA9eb0PJYuHKNaHPguz077xPQyge6pbPjggRILQC7mZAqP4&rsv_dl=re_dqa_generate&sa=re_dqa_generate)中创建分屏可以通过以下命令实现**‌==：‌12

- ==‌**水平分屏**‌==：使用 `:sp [文件名]` 命令可以在水平方向上增加一个分屏，同时编辑多个文件。
- ==‌**垂直分屏**‌==：使用 `:vsp [文件名]` 命令可以在垂直方向上增加一个分屏，同时编辑多个文件。

==‌**在分屏中的操作命令包括**‌==：

- ==‌**切换到下一个分屏**‌==：按下 `Ctrl + w` 后再按 `j` 可以切换到下一个分屏。
- ==‌**关闭当前分屏**‌==：按下 `Ctrl + w` 后再按 `c` 可以关闭当前分屏（但不能关闭最后一个分屏）。
- ==‌**退出当前分屏**‌==：按下 `Ctrl + w` 后再按 `q` 可以退出当前分屏（如果是最后一个分屏，则关闭 Vim 编辑器）。
- ==‌**互换分屏**‌==：按下 `Ctrl + w` 后再按 `r` 可以互换两个分屏的内容。

==‌**Vim 分屏的实用技巧和常见问题解决方法包括**‌==：

- ==‌**创建空白分屏**‌==：使用 `:new` 命令可以创建一个新的空白分屏。
- ==‌**关闭所有分屏**‌==：按下 `Ctrl + w` 后再按 `o` 可以关闭所有分屏，只保留当前分屏。