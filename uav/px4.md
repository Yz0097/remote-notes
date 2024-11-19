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

## px4 make taargets
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
