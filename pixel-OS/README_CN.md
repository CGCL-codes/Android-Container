# PixelExperience

本项目用到的操作系统是PixelExperience，安卓10版本，用到的设备是红米k20 pro。下面讲述如何编译PixelExperience，这是安卓中运行容器的第一步。之后便是修改内核，以满足docker和criu需要的内核环境。

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