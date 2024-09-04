#git #coding 
This is a remote repositroy for notes.    

Store it on github for:
- learn to use git
- access to note with more terminal device

## how to use
### 1. 克隆笔记本到本地
添加ssh密钥到github账号，参考[[ssh key]]    
进入本地存储位置，执行
```
git clone git@github.com:Yz0097/remote-notes.git
```

或者使用合并远程仓库的方法，在对应本地仓库
```
git remote add <origin (远程仓库别名)> <url>
git pull --rebase <origin (远程仓库别名)> master
```

特别的注意，每次开始前最好首先保证可以连接到github，执行pull同步github上的内容。

### 2. 提交单次笔记的内容

```
git add .
git commit -m "brief note content"
git push origin master
```
