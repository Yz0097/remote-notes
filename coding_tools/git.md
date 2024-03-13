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
git commit <-m "***"> <-a> // -a == git add . , git commit
git log <--oneline>
git rm <file> <--cache>
```

### gitignore

利用".gitignore"文件可以在git中忽略     
注意先提交到git中再在ignore中添加是无效的

### remote 
```
git remote add <origin (远程仓库别名)> <url>
git remote -v //用于查看
git push <-u(upstream)> <origin> <main(:main)>
```

### 分支

```
git switch <branch name>
git merge dev //合并dev分支和当前分支
git log --graph --oneline
git branch <branch name>//查看分支 or 创建分支
git branch -d <branch name> //删除已经合并的分支
gir branch -D <> //强制删除分支
```

### 冲突
merge产生冲突时，修改冲突内容然后提交。     
中止冲突：
```
git merge --abort
```

```
git rebase main
git rebase dev
```

# GitFlow

main hotfix release devlop feature

feature 从 dev 中分离
dev中发布 release 进行测试，测试后合并到 main

GIthubFlow
Pull Request
