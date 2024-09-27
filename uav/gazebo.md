报错
```
[Err] [Master.cc:96] EXCEPTION: Unable to start server[bind: Address already in use]. There is probably another Gazebo process running.
 
[Err] [Master.cc:96] EXCEPTION: Unable to start server[bind: Address already in use]. There is probably another Gazebo process running.
```
https://blog.csdn.net/liushidu123/article/details/108533725
解决方法:
```
killall gzserver
killall gzclient
```

ardupilot/Tools/autotest/default_params/copter.param
添加ARMING_CHECK参数设置为0 禁用arming check，防止出现main loop slow错误