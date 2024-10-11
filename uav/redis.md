### redis远程链接数据库
`redis-cli -h [host_ip] -p [prot]`
进入客户端后`ping`测试是否连通，返回`PONG`


```Python
## 测试是否能够远程链接
import redis
r=redis.Redis(host='192.168.1.104',port=6379,db=0,password='xd173' )
try:
    r.ping()
    print("1")
except:
    print("0")
```

redis配置文件位置
/etc/redis/redis.conf