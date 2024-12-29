https://docs.px4.io/main/en/sim_gazebo_classic/#installation
px4飞控官网教程
# 安装
ubuntu20.04 lts
Gazebo classic
如果使用22.04需要安装新版本Gazebo(Harmonic)
```bash
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
// --recursive:递归克隆所有的代码
```


```bash
make px4_sitl gazebo-classic
pxh> commander takeoff

```

## px4 make targets
```bash
make [VENDOR_][MODEL][_VARIANT] [VIEWER_MODEL_DEBUGGER_WORLD]
```

- **VENDOR_MODEL_VARIANT**: (also known as `CONFIGURATION_TARGET`)
- **VENDOR:** The manufacturer of the board: `px4`, `aerotenna`, `airmind`, `atlflight`, `auav`, `beaglebone`, `intel`, `nxp`, etc. The vendor name for Pixhawk series boards is `px4`.
- **MODEL:** The _board model_ "model": `sitl`, `fmu-v2`, `fmu-v3`, `fmu-v4`, `fmu-v5`, `navio2`, etc.
- **VARIANT:** Indicates particular configurations: e.g. `bootloader`, `cyphal`, which contain components that are not present in the `default` configuration. Most commonly this is `default`, and may be omitted.

```bash
make list_config_targets
```
列出所有选项


# sitl - default

```shell
syz@ubuntu:~/PX4-Autopilot$ make -n px4_sitl gazebo-classic
# check if the desired cmake configuration matches the cache then CMAKE_CACHE_CHECK stays empty
# change to build folder which fails if it doesn't exist and CACHED_CMAKE_OPTIONS stays empty
# fetch all previously configured and cached options from the build folder and transform them into the OPTION=VALUE format without type (e.g. :BOOL)
# transform the options in CMAKE_ARGS into the OPTION=VALUE format without -D
# find each currently desired option in the already cached ones making sure the complete configured string value is the same
# if the complete list of desired options is found in the list of verified options we don't need to reconfigure and CMAKE_CACHE_CHECK stays empty
# make sure to start from scratch when switching from GNU Make to Ninja
if [ Ninja = "Ninja" ] && [ -e "/home/syz/PX4-Autopilot/build/px4_sitl_default"/Makefile ]; then rm -rf "/home/syz/PX4-Autopilot/build/px4_sitl_default"; fi
# make sure to start from scratch if ninja build file is missing
if [ Ninja = "Ninja" ] && [ ! -f "/home/syz/PX4-Autopilot/build/px4_sitl_default"/build.ninja ]; then rm -rf "/home/syz/PX4-Autopilot/build/px4_sitl_default"; fi
# only excplicitly configure the first build, if cache file already exists the makefile will rerun cmake automatically if necessary
if [ ! -e "/home/syz/PX4-Autopilot/build/px4_sitl_default"/CMakeCache.txt ] || [  ]; then mkdir -p "/home/syz/PX4-Autopilot/build/px4_sitl_default" && cd "/home/syz/PX4-Autopilot/build/px4_sitl_default" && cmake "/home/syz/PX4-Autopilot" -G"Ninja"  -DCONFIG=px4_sitl_default || (rm -rf "/home/syz/PX4-Autopilot/build/px4_sitl_default"); fi
# run the build for the specified target
cmake --build "/home/syz/PX4-Autopilot/build/px4_sitl_default" --  gazebo-classic
```

## ardupilot-gazebo运行脚本
- Open a terminal and run the commands below:
```
cd ~/uav/ardupilot/Tools/autotest
./sim_vehicle.py -v ArduCopter -f gazebo-iris --console -I0
```
- Open a new terminal and run:
```
gazebo --verbose ~/uav/ardupilot_gazebo/worlds/iris_ardupilot.world
```
- After seeing "APM: EKF2 IMU0 is using GPS" message in console, you can use the commands below in the first terminal for takeoff test:
```
mode guided
arm throttle
takeoff 5
```

# wind plug
Tools/simulation/gazebo-classic/worlds中修改
empty.world修改为
```xml
    <include>
      <uri>model://sun</uri>
    </include>
    <!-- A ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://asphalt_plane</uri>
    </include>
    <plugin name='wind_plugin' filename='libgazebo_wind_plugin.so'>
      <frameId>base_link</frameId>
      <robotNamespace/>
      <windVelocityMean>15.0</windVelocityMean>
      <windVelocityMax>20.0</windVelocityMax>
      <windVelocityVariance>0</windVelocityVariance>
      <windDirectionMean>0 1 0</windDirectionMean>
      <windDirectionVariance>0</windDirectionVariance>
      <windGustStart>0</windGustStart>
      <windGustDuration>0</windGustDuration>
      <windGustVelocityMean>0</windGustVelocityMean>
      <windGustVelocityMax>20.0</windGustVelocityMax>
      <windGustVelocityVariance>0</windGustVelocityVariance>
      <windGustDirectionMean>1 0 0</windGustDirectionMean>
      <windGustDirectionVariance>0</windGustDirectionVariance>
      <windPubTopic>world_wind</windPubTopic>
    </plugin>
    <physics name='default_physics' default='0' type='ode'>
      <gravity>0 0 -9.8066</gravity>
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>
          <sor>1.3</sor>
          <use_dynamic_moi_rescaling>0</use_dynamic_moi_rescaling>
        </solver>
        <constraints>
          <cfm>0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
      <max_step_size>0.004</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>250</real_time_update_rate>
      <magnetic_field>6.0e-6 2.3e-5 -4.2e-5</magnetic_field>
    </physics>
  </world>
</sdf>
```

修改部分在于其中一个插件
```xml
<plugin name='wind_plugin' filename='libgazebo_wind_plugin.so'>
  <frameId>base_link</frameId>
  <robotNamespace/>
  <windVelocityMean>15.0</windVelocityMean>
  <windVelocityMax>20.0</windVelocityMax>
  <windVelocityVariance>0</windVelocityVariance>
  <windDirectionMean>0 1 0</windDirectionMean>
  <windDirectionVariance>0</windDirectionVariance>
  <windGustStart>0</windGustStart>
  <windGustDuration>0</windGustDuration>
  <windGustVelocityMean>0</windGustVelocityMean>
  <windGustVelocityMax>20.0</windGustVelocityMax>
  <windGustVelocityVariance>0</windGustVelocityVariance>
  <windGustDirectionMean>1 0 0</windGustDirectionMean>
  <windGustDirectionVariance>0</windGustDirectionVariance>
  <windPubTopic>world_wind</windPubTopic>
</plugin>
```
修改`windVelocityMean`和`windVelocityMax`, 平均值应该小于最大值.
velocity variance风速变量的单位是$(m/s)^2$
方向变量基于正态分布, 将扰动添加到模拟中.
Gust 狂风.`windGustStart`和`windGustDuration`决定了狂风的开始时间和持续时间

# commander
px4终端中
`commander takeoff`
`commander land`


```bash
cd /home/syz/PX4-Autopilot/build/px4_sitl_defau...X4-Autopilot /home/syz/PX4-Autopilot/build/px4_sitl_default
SITL ARGS
sitl_bin: /home/syz/PX4-Autopilot/build/px4_sitl_default/bin/px4
debugger: none
model: iris
world: none
src_path: /home/syz/PX4-Autopilot
build_path: /home/syz/PX4-Autopilot/build/px4_sitl_default
GAZEBO_PLUGIN_PATH :/home/syz/PX4-Autopilot/build/px4_sitl_default/build_gazebo-classic
GAZEBO_MODEL_PATH :/home/syz/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models
LD_LIBRARY_PATH :/home/syz/PX4-Autopilot/build/px4_sitl_default/build_gazebo-classic
empty world, setting empty.world as default
Using: /home/syz/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris/iris.sdf
Error Code 12 Msg: Unable to find uri[model://gps]
SITL COMMAND: "/home/syz/PX4-Autopilot/build/px4_sitl_default/bin/px4" "/home/syz/PX4-Autopilot/build/px4_sitl_default"/etc

______  __   __    ___ 
| ___ \ \ \ / /   /   |
| |_/ /  \ V /   / /| |
|  __/   /   \  / /_| |
| |     / /^\ \ \___  |
\_|     \/   \/     |_/

px4 starting.

INFO  [px4] startup script: /bin/sh etc/init.d-posix/rcS 0
INFO  [init] found model autostart file as SYS_AUTOSTART=10015
INFO  [param] selected parameter default file parameters.bson
INFO  [param] importing from 'parameters.bson'
INFO  [parameters] BSON document size 404 bytes, decoded 404 bytes (INT32:14, FLOAT:6)
INFO  [param] selected parameter backup file parameters_backup.bson
Gazebo multi-robot simulator, version 11.14.0
Copyright (C) 2012 Open Source Robotics Foundation.
Released under the Apache 2 License.
http://gazebosim.org

[Msg] Waiting for master.
[Msg] Connected to gazebo master @ http://127.0.0.1:11345
[Msg] Publicized address: 192.168.137.19
INFO  [dataman] data manager file './dataman' size is 7872608 bytes
INFO  [init] PX4_SIM_HOSTNAME: localhost
INFO  [simulator_mavlink] Waiting for simulator to accept connection on TCP port 4560

```