#git #coding 
## 初始化

```
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global user.name ziiz
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global user.email coppton.ii@gmail.com
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global list
error: key does not contain a section: list
root@iZbp1a9zt2ii9pe3pzmagsZ:/# git config --global --list
user.name=ziiz
user.email=coppton.ii@gmail.com
```

```
git init <repositroy name>
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
git branch -D <> //强制删除分支
git chechout <branch_name>
```
git clone 只会克隆master分支, 使用git branch -a 可以查看远程仓库上的所有分支,使用checkout可以切换到远程仓库上的分支(克隆到本地)
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

### Github Flow    
Pull   
Request

# windows & linux换行符不一致
git config --global core.autocrlf false


# git clone 失败
```bash
failed to connect to github.com port 443 after 21136 ms: couldn‘t connect to server
```

windows设置 -> 网络 -> 代理 -> 手动设置代理 -> 端口 : 4780
在git bash 中:
```bash
git config --global http.proxy 127.0.0.1:4780
git config --global https.proxy 127.0.0.1:4780
```