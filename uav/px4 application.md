# example: minmal application
https://docs.px4.io/main/en/modules/hello_sky.html
./PX4_AUTOPILOT/src/examples/下的文件夹内建立新的文件夹，例如
```bash
mkdir my_app
```
最小情况下包含三个文件`CMakeLists.txt`,`my_app.c`,`Kconfig`
此章节针对sitl(Software In The Loop)情况
## 1. my_app.c
```C
/**
 * @file px4_simple_app.c
 * Minimal application example for PX4 autopilot
 *
 * @author Example User <mail@example.com>
 */

#include <px4_platform_common/log.h>

__EXPORT int px4_simple_app_main(int argc, char *argv[]);

int px4_simple_app_main(int argc, char *argv[])
{
	PX4_INFO("Hello Sky!");
	return OK;
}
```
主函数的名字应为`<module_name>_main`
## 2. CMakeList.c
```C
px4_add_module(
	MODULE examples__my_app
	MAIN my_app
	STACK_MAIN 2000
	SRCS
		my_app.c
	DEPENDS
	)
```

`PX4-Autopilot/cmake/px4_add_module.cmake`中定义了px4_add_module
## 3. Kconfig
```C
menuconfig EXAMPLES_MY_APP
	bool "my_app"
	default n
	---help---
		Enable support for my_app
```
Kconfig的命名惯例：`EXAMPLES_MY_APP`对应文件夹`./PX4_AUTOPILOT/src/examples/my_app`
## 4. 编译运行
在`PX4-Autopilot/boards/px4/sitl/default.px4board`下添加参数（针对不同的硬件版本，仿真环境，board文件不同）
```
CONFIG_PLATFORM_POSIX=y
CONFIG_BOARD_TESTING=y

... ...
CONFIG_EXAMPLES_PX4_SIMPLE_APP=y
//官方示例，切换为n可以不编译这一个示例
... ...

CONFIG_EXAMPLES_MY_APP=Y
```
在`CMakeLists.txt`中设置dyn参数可以将模块设置为dynamic，在一个额外的文件夹中生成编译文件
```bash
make px4_sitl gazebo-classic
```
编译运行当前环境