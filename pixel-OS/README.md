# PixelExperience

**English** | [中文](README_CN.md)

The operating system used in this project is PixelExperience, Android 10 version, and the device used is Redmi k20 pro. The following describes how to compile PixelExperience, which is the first step to run a container in Android. After that is to modify the kernel to meet the kernel environment required by docker and criu.

The diff file is in the files directory, which is aosp.diff.



My building environment:

- Ubuntu18.04
- 300GB of free storage
- Redmi K20 Pro

### build environment

```shell
# Open ternimal and enter the following:
sudo apt-get install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev
```

### Sync

```shell
First,you need to install repo by youself.
mkdir k20pro
cd k20pro
# Initialize local repository
repo init -u https://github.com/PixelExperience/manifest -b ten

# Sync
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags
```

### Kernel

```bash
#use F1xy kernel
mkdir -p kernel/xiaomi/raphael
git clone https://github.com/PixelExperience-Devices/kernel_xiaomi_raphael kernel/xiaomi/raphael
#Use building kernel instead of prebuilt kernel,this step requires lunch aosp_raphael-eng first.
#Modify file BoardConfig.mk,Comment out 
#TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/kernel
vim device/xiaomi/raphael/BoardConfig.mk
#Modify file kernel.mk
vim vendor/aosp/build/tasks/kernel.mk
#define this:
TARGET_KERNEL_CONFIG = raphael_defconfig
```

### Build

```bash
# Set up environment
$ . build/envsetup.sh

# Choose a target,redmi k20 pro has user,userdebug,eng
$ lunch aosp_raphael-eng

# Build the code
$ mka bacon -jX
```

### Errors

```
if you encounter `out of memory`,Expand your swap space.
```

### Root permissions

You need to obtain root permissions and swipe into the magisk installation package by swiping the card. The download address of magisk is: [magisk](https://github.com/topjohnwu/Magisk/releases).

\### Flashing ROM package We provide a compiled ROM package, which is only suitable for Redmi K20 Pro phones, which contains the environment for running Docker and criu, criu needs to manually copy the files to the /criu directory, and the docker binary file is already included in the /bin directory Next, the tar file needs to be copied manually. **note! ! ! **Refreshing is risky, operation should be done carefully. You need to flash the miui_RAPHAEL_V12.0.5.0.QFKCNXM_d03168fb55_10.0.zip flashing package first, and then flashing PixelExperience_raphael-10.0-20201204-0354-UNOFFICIAL-48bit-docker-criu.zip, the flashing method is card. ROM download address, Google Cloud Disk:



1.[PixelExperience_raphael-10.0-20201204-0354-UNOFFICIAL-48bit-docker-criu.zip](https://drive.google.com/file/d/1khrsGkcuxamdZbyMIwVg8r9PIF6IUcRz/view?usp=sharing)

2.[miui_RAPHAEL_V12.0.5.0.QFKCNXM_d03168fb55_10.0.zip](https://drive.google.com/file/d/1T39MsduE7rZDX6gdaeFwfjEfgKbxvLSU/view?usp=sharing)