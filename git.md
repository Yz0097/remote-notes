```
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global user.name ziiz
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global user.email coppton.ii@gmail.com
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global list
error: key does not contain a section: list
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global --list
user.name=ziiz
user.email=coppton.ii@gmail.com
```

### git 工作区域
工作区域 - 暂存区 - 本地仓库     
working dic - index - local repesitory
### git 文件状态

untrack unmodified modified staged

### git 提交
常用指令
```
git add .
git ls-files
git commit <-m "***">
git log <--oneline>
git rm <file> <--cache>
```

### gitignore

利用".gitignore"文件可以在git中忽略     
注意先提交到git中再在ignore中添加是无效的