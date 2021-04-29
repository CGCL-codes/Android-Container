# PixelExperience

本项目用到的操作系统是PixelExperience，安卓10版本，用到的设备是红米k20 pro。下面讲述如何编译PixelExperience，这是安卓中运行容器的第一步。之后便是修改内核，以满足docker和criu需要的内核环境。

修改的diff文件在files目录下，名为aosp.diff。



我的编译环境和安卓设备:

- Ubuntu18.04
- 300GB的硬盘空间
- Redmi K20 Pro

### 安装依赖

```
# Open ternimal and enter the following:
sudo apt-get install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev
```

### 同步PixelExperience源码

```
# First,you need to install repo by youself.
mkdir k20pro
cd k20pro
# Initialize local repository
repo init -u https://github.com/PixelExperience/manifest -b ten

# Sync
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags
```

### Kernel

```bash
# 使用 F1xy 内核
mkdir -p kernel/xiaomi/raphael
git clone https://github.com/PixelExperience-Devices/kernel_xiaomi_raphael kernel/xiaomi/raphael
# 使用自己编译内核代替默认编译的内核
# 修改文件BoardConfig.mk，然后注释下面那一行代码
# TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/kernel
vim device/xiaomi/raphael/BoardConfig.mk
# 修改文件kernel.mk
vim vendor/aosp/build/tasks/kernel.mk
# 定义内核配置文件
TARGET_KERNEL_CONFIG = raphael_defconfig
```

### 编译

```bash
# 设置环境变量
$ . build/envsetup.sh

# 选择编译的AOSP版本，这里使用eng版本，拥有root权限
$ lunch aosp_raphael-eng

# 编译系统
$ mka bacon -jX
```

### 错误

```
如果遇到 `out of memory`，是内存不足够编译，可以增加swap的空间大小
```

### Root权限

需要获取到root权限，通过卡刷刷入magisk安装包，magisk的下载地址：[magisk](https://github.com/topjohnwu/Magisk/releases)。

### 刷机ROM包

我们提供了一个编译好的ROM包，该ROM包仅仅适用于Redmi K20 Pro手机，里面含有运行Docker和criu的环境，criu需要手动复制文件到/criu目录，docker的二进制文件已经包含在/bin目录下，tar文件需要自己手动复制。**注意！！！**刷机有风险，操作需谨慎。

你需要先刷入miui_RAPHAEL_V12.0.5.0.QFKCNXM_d03168fb55_10.0.zip刷机包，然后再刷入PixelExperience_raphael-10.0-20201204-0354-UNOFFICIAL-48bit-docker-criu.zip，刷机方式为卡刷。

ROM下载地址，Google云盘：

1.[PixelExperience_raphael-10.0-20201204-0354-UNOFFICIAL-48bit-docker-criu.zip](https://drive.google.com/file/d/1khrsGkcuxamdZbyMIwVg8r9PIF6IUcRz/view?usp=sharing)

2.[miui_RAPHAEL_V12.0.5.0.QFKCNXM_d03168fb55_10.0.zip](https://drive.google.com/file/d/1T39MsduE7rZDX6gdaeFwfjEfgKbxvLSU/view?usp=sharing)

