#coding #git
### 生成ssh密钥
```
ssh-keygen -t rsa -b 4096
```
随后输入密钥文件名，或者采用默认设置

### 配置config文件
```
##########SSH for github###########
Host github.com
HostName github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/ssh_key_for_github
################################
```
