## Run Docker on Android

**English** | [中文](README_CN.md)

These files are docker static binary. Version is 19.03.6. 

### Step

-----

#### 1. compile Android linux kernel

The Android system has tailored the kernel by default, but running the container requires the support of many kernel features, so the kernel needs to be compiled. Your kernel needs to have the following kernel configuration options:

|     Kernel configuration items      |                    explain                     |
| :---------------------------------: | :--------------------------------------------: |
|          CONFIG_NAMESPACES          |                   Namespaces                   |
|            CONFIG_NET_NS            |               Network namespace                |
|            CONFIG_PID_NS            |                 PID namespace                  |
|            CONFIG_IPC_NS            |                 IPC namespace                  |
|            CONFIG_UTS_NS            |                 UTS namespace                  |
|           CONFIG_CGROUPS            |              cgroup control group              |
|        CONFIG_CGROUP_CPUACCT        |           cgroup's cpuacct subsystem           |
|        CONFIG_CGROUP_DEVICE         |           cgroup's device subsystem            |
|        CONFIG_CGROUP_FREEZER        |           cgroup's freezer subsystem           |
|         CONFIG_CGROUP_SCHED         |            cgroup's sched subsystem            |
|           CONFIG_CPUSETS            |           cgroup's cpuset subsystem            |
|            CONFIG_MEMCG             |            cgroup's memcg subsystem            |
|             CONFIG_KEYS             |          Access key retention support          |
|             CONFIG_VETH             |           Virtual Ethernet to Device           |
|            CONFIG_BRIDGE            |            802.1d Ethernet bridging            |
|       CONFIG_BRIDGE_NETFILTER       |         Bridge IP/ARP packet filtering         |
|         CONFIG_NF_NAT_IPV4          |        IPv4 virtual address translation        |
|         CONFIG_IP_NF_FILTER         |              IP packet filtering               |
|   CONFIG_IP_NF_TARGET_MASQUERADE    |           MASQUERADE target support            |
| CONFIG_NETFILTER_XT_MATCH_ADDRTYPE  |     addrtype address type matching support     |
| CONFIG_NETFILTER_XT_MATCH_CONNTRACK | Conntrack connection tracking matching support |
|   CONFIG_NETFILTER_XT_MATCH_IPVS    |             ipvs matching support              |
|          CONFIG_IP_NF_NAT           |  iptables virtual address translation support  |
|        CONFIG_NF_NAT_NEEDED         |      Virtual address translation related       |
|         CONFIG_POSIX_MQUEUE         |              POSIX message queue               |
|          CONFIG_OVERLAY_FS          |          overlay file system support           |
|             CONFIG_AIO              |         POSIX asynchronous IO support          |
|             CONFIG_TTY              |           Enable character terminal            |

Steps to compile the kernel and add kernel compilation options:

```shell
# Enter the root directory of the kernel source code
cd /kenel/k20pro
# Use the specified configuration file raphael_defconfig, the configuration file is in arch/x86/configs
make raphael_defconfig
# Use a graphical way to add kernel compilation options, add each of the above options, you can use the "/" corresponding button to search for the location of the kernel option
make menuconfig
# Compile the kernel
make -j4 
```

------

#### 2. Modify cpuset.c code

Because Android removes the prefix cpuset of the cpuset subsystem by default, but Docker requires this part of the prefix, so you need to modify the cpuset.c source code in the cgroup to add this part of the prefix. The location of the file is: kernel/cgroup/cpuset.c, the modified content is:

```c
diff --git a/kernel/cgroup/cpuset.c b/kernel/cgroup/cpuset.c
index d50a89ccfe99..c86c17d16892 100644
--- a/kernel/cgroup/cpuset.c
+++ b/kernel/cgroup/cpuset.c
@@ -1937,6 +1937,106 @@ static struct cftype files[] = {
                .private = FILE_MEMORY_PRESSURE_ENABLED,
        },


   /* patch */
   {
           .name = "cpuset.cpus",
           .seq_show = cpuset_common_seq_show,
           .write = cpuset_write_resmask,
           .max_write_len = (100U + 6 * NR_CPUS),
           .private = FILE_CPULIST,
   },

   {
           .name = "cpuset.mems",
           .seq_show = cpuset_common_seq_show,
           .write = cpuset_write_resmask,
           .max_write_len = (100U + 6 * MAX_NUMNODES),
           .private = FILE_MEMLIST,
   },

   {
           .name = "cpuset.effective_cpus",
           .seq_show = cpuset_common_seq_show,
           .private = FILE_EFFECTIVE_CPULIST,
   },

   {
           .name = "cpuset.effective_mems",
           .seq_show = cpuset_common_seq_show,
           .private = FILE_EFFECTIVE_MEMLIST,
   },

   {
           .name = "cpuset.effective_mems",
           .seq_show = cpuset_common_seq_show,
           .private = FILE_EFFECTIVE_MEMLIST,
   },

   {
           .name = "cpuset.cpu_exclusive",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_CPU_EXCLUSIVE,
   },

   {
           .name = "cpuset.mem_exclusive",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_MEM_EXCLUSIVE,
   },

   {
           .name = "cpuset.mem_hardwall",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_MEM_HARDWALL,
   },

   {
           .name = "cpuset.sched_load_balance",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_SCHED_LOAD_BALANCE,
   },

   {
           .name = "cpuset.sched_relax_domain_level",
           .read_s64 = cpuset_read_s64,
           .write_s64 = cpuset_write_s64,
           .private = FILE_SCHED_RELAX_DOMAIN_LEVEL,
   },

   {
           .name = "cpuset.memory_migrate",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_MEMORY_MIGRATE,
   },

   {
           .name = "cpuset.memory_pressure",
           .read_u64 = cpuset_read_u64,
           .private = FILE_MEMORY_PRESSURE,
   },

   {
           .name = "cpuset.memory_spread_page",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_SPREAD_PAGE,
   },
   {
           .name = "cpuset.memory_spread_slab",
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_SPREAD_SLAB,
   },

   {
           .name = "cpuset.memory_pressure_enabled",
           .flags = CFTYPE_ONLY_ON_ROOT,
           .read_u64 = cpuset_read_u64,
           .write_u64 = cpuset_write_u64,
           .private = FILE_MEMORY_PRESSURE_ENABLED,
   },
   /* patch */
```

It should be noted that when modifying, the above content is copied from the modified file, and then the `cpuset.` prefix is added.

-----

#### 3. Download the Docker binary file

After all the above are modified, there is kernel feature support for running the container, and then download the static binary files of Docker, and then copy them all to the /bin directory, and add the execution permission, then they can be directly called, [download address ](https://download.docker.com/linux/static/stable/aarch64/). 

-----

#### 4. Modify read and write permissions

Because some read-only file directories are currently used, the read and write permissions of the file system need to be modified. You can connect the mobile phone through the adb tool, and then enter `adb remount` to modify the file system to be readable and writable.

------

#### 5. Mount all cgroup subsystems

Modify the /etc/cgroup.json file of the Android operating system to the following content to mount all cgroup subsystems. 

```json
{"Cgroups":[{"UID":"system","GID":"system","Mode":"0755","Controller":"blkio","Path":"/dev/blkio"},{"UID":"system","GID":"system","Mode":"0755","Controller":"cpu","Path":"/dev/cpu"},{"Mode":"0555","Path":"/dev/cpuacct","Controller":"cpuacct"},{"UID":"system","GID":"system","Mode":"0755","Controller":"cpuset","Path":"/dev/cpuset"},{"UID":"system","GID":"system","Mode":"0755","Controller":"memory","Path":"/dev/memcg"},{"UID":"system","GID":"system","Mode":"0755","Controller":"schedtune","Path":"/dev/stune"},{"GID":"system","UID":"system","Mode":"0755","Controller":"devices","Path":"/dev/devices"},{"GID":"system","UID":"system","Mode":"0755","Controller":"freezer","Path":"/dev/freezer"},{"GID":"system","UID":"system","Mode":"0755","Controller":"hugetlb","Path":"/dev/hugetlb"},{"GID":"system","UID":"system","Mode":"0755","Controller":"net_cls","Path":"/dev/net_cls"},{"GID":"system","UID":"system","Mode":"0755","Controller":"net_prio","Path":"/dev/net_prio"},{"GID":"system","UID":"system","Mode":"0755","Controller":"perf_event","Path":"/dev/perf_event"},{"GID":"system","UID":"system","Mode":"0755","Controller":"pids","Path":"/dev/pids"},{"GID":"system","UID":"system","Mode":"0755","Controller":"rdma","Path":"/dev/rdma"}],"Cgroups2":{"UID":"root","GID":"root","Mode":"0600","Path":"/dev/cg2_bpf"}}
```

In order to facilitate viewing, format the json data as follows:

```json
{
  "Cgroups": [
    {
      "UID": "system",
      "GID": "system",
      "Mode": "0755",
      "Controller": "blkio",
      "Path": "/dev/blkio"
    },
    {
      "UID": "system",
      "GID": "system",
      "Mode": "0755",
      "Controller": "cpu",
      "Path": "/dev/cpu"
    },
    {
      "Mode": "0555",
      "Path": "/dev/cpuacct",
      "Controller": "cpuacct"
    },
    {
      "UID": "system",
      "GID": "system",
      "Mode": "0755",
      "Controller": "cpuset",
      "Path": "/dev/cpuset"
    },
    {
      "UID": "system",
      "GID": "system",
      "Mode": "0755",
      "Controller": "memory",
      "Path": "/dev/memcg"
    },
    {
      "UID": "system",
      "GID": "system",
      "Mode": "0755",
      "Controller": "schedtune",
      "Path": "/dev/stune"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "devices",
      "Path": "/dev/devices"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "freezer",
      "Path": "/dev/freezer"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "hugetlb",
      "Path": "/dev/hugetlb"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "net_cls",
      "Path": "/dev/net_cls"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "net_prio",
      "Path": "/dev/net_prio"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "perf_event",
      "Path": "/dev/perf_event"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "pids",
      "Path": "/dev/pids"
    },
    {
      "GID": "system",
      "UID": "system",
      "Mode": "0755",
      "Controller": "rdma",
      "Path": "/dev/rdma"
    }
  ],
  "Cgroups2": {
    "UID": "root",
    "GID": "root",
    "Mode": "0600",
    "Path": "/dev/cg2_bpf"
  }
}
```

------

#### 6. Start Docker with a script

Docker requires some file directories when running. Android does not have these file directories by default, so they are created using script files. And due to the lack of IP routing rules, two rules need to be added. In addition, SELinux needs to be turned off, and only some files and directories can be accessed after it is turned off.

It is worth mentioning that, in order to use the crun container to run, you need to mount the cgroup to /sys/fs/cgroup, so add this part of the content to the script file. The content of the script file is as follows:

```shell
#!/system/bin/sh

mount -o rw,remount /
# mkdir on /system
if [ ! -d "/system/etc/docker" ]; then
        mkdir /system/etc/docker
fi

# mkdir on /
if [ ! -d "/var" ]; then
        mkdir /var
fi
if [ ! -d "/run" ]; then
        mkdir /run
fi
if [ ! -d "/tmp" ]; then
        mkdir /tmp
fi
if [ ! -d "/opt" ]; then
        mkdir /opt
fi
if [ ! -d "/usr" ]; then
        mkdir /usr
fi
# mkdir on /data
if [ ! -d "/data/var" ]; then
        mkdir /data/var
else
        rm -rf /data/var/run
fi
if [ ! -d "/data/run" ]; then
        mkdir /data/run
fi
if [ ! -d "/data/tmp" ]; then
        mkdir /data/tmp
fi
if [ ! -d "/data/opt" ]; then
        mkdir /data/opt
fi
if [ ! -d "/data/etc" ]; then
        mkdir /data/etc
        mkdir /data/etc/docker
fi

# Create some directories in /dev
# if [ ! -d "/dev/freezer" ]; then
        # mkdir /dev/blkio
        # mkdir /dev/cpu
        # mkdir /dev/cpuacct
        # mkdir /dev/cpuset
        # mkdir /dev/devices
        # mkdir /dev/freezer
        # mkdir /dev/hugetlb
        # mkdir /dev/memory
        # mkdir /dev/net_cls
        # mkdir /dev/net_prio
        # mkdir /dev/perf_event
        # mkdir /dev/pids
        # mkdir /dev/rdma
        # mkdir /dev/stune
# fi

mount tmpfs /sys/fs/cgroup -t tmpfs -o size=1G
if [ ! -d "/sys/fs/cgroup/blkio" ]; then
        mkdir /sys/fs/cgroup/blkio
        mkdir /sys/fs/cgroup/cpu
        mkdir /sys/fs/cgroup/cpuacct
        mkdir /sys/fs/cgroup/cpuset
        mkdir /sys/fs/cgroup/devices
        mkdir /sys/fs/cgroup/freezer
        mkdir /sys/fs/cgroup/hugetlb
        mkdir /sys/fs/cgroup/memory
        mkdir /sys/fs/cgroup/net_cls
        mkdir /sys/fs/cgroup/net_prio
        mkdir /sys/fs/cgroup/perf_event
        mkdir /sys/fs/cgroup/pids
        mkdir /sys/fs/cgroup/rdma
        mkdir /sys/fs/cgroup/schedtune
        mkdir /sys/fs/cgroup/systemd
fi

# mount --bind
mount --bind /data/etc/docker /etc/docker
mount --bind /data/var /var
mount --bind /data/run /run
mount --bind /data/tmp /tmp
mount --bind /data/opt /opt


# mount cgroup to /dev
# mount -t cgroup -o blkio none /dev/blkio
# mount -t cgroup -o cpu none /dev/cpu
# mount -t cgroup -o cpuacct none /dev/cpuacct
# mount -t cgroup -o cpuset none /dev/cpuset
# mount -t cgroup -o devices none /dev/devices
# mount -t cgroup -o freezer none /dev/freezer
# mount -t cgroup -o hugetlb none /dev/hugetlb
# mount -t cgroup -o memory none /dev/memory
# mount -t cgroup -o net_cls none /dev/net_cls
# mount -t cgroup -o net_prio none /dev/net_prio
# mount -t cgroup -o perf_event none /dev/perf_event
# mount -t cgroup -o pids none /dev/pids
# mount -t cgroup -o rdma none /dev/rdma
# mount -t cgroup -o schedtune none /dev/stune

mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd
mount -t cgroup -o blkio,nodev,noexec,nosuid cgroup /sys/fs/cgroup/blkio
mount -t cgroup -o cpu,nodev,noexec,nosuid cgroup /sys/fs/cgroup/cpu
mount -t cgroup -o cpuacct,nodev,noexec,nosuid cgroup /sys/fs/cgroup/cpuacct
mount -t cgroup -o cpuset,nodev,noexec,nosuid cgroup /sys/fs/cgroup/cpuset
mount -t cgroup -o devices,nodev,noexec,nosuid cgroup /sys/fs/cgroup/devices
mount -t cgroup -o freezer,nodev,noexec,nosuid cgroup /sys/fs/cgroup/freezer
mount -t cgroup -o hugetlb,nodev,noexec,nosuid cgroup /sys/fs/cgroup/hugetlb
mount -t cgroup -o memory,nodev,noexec,nosuid cgroup /sys/fs/cgroup/memory
mount -t cgroup -o net_cls,nodev,noexec,nosuid cgroup /sys/fs/cgroup/net_cls
mount -t cgroup -o net_prio,nodev,noexec,nosuid cgroup /sys/fs/cgroup/net_prio
mount -t cgroup -o perf_event,nodev,noexec,nosuid cgroup /sys/fs/cgroup/perf_event
mount -t cgroup -o pids,nodev,noexec,nosuid cgroup /sys/fs/cgroup/pids
mount -t cgroup -o rdma,nodev,noexec,nosuid cgroup /sys/fs/cgroup/rdma
mount -t cgroup -o schedtune,nodev,noexec,nosuid cgroup /sys/fs/cgroup/schedtune

# ip route
ip rule add pref 1 from all lookup main
ip rule add pref 2 from all lookup default
###
# setup dns nameserver and docker images registry
echo "{\"registry-mirrors\":[\"https://docker.mirrors.ustc.edu.cn\"],\"experimental\":true}" > /etc/docker/daemon.json
# open br_netfilter module
# modprobe br_netfilter
setenforce 0
# run dockerd
export DOCKER_RAMDISK=true
#dockerd --add-runtime crun=/bin/crun -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock > /dev/null 2>&1 &
dockerd --add-runtime crun=/bin/crun -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock &
```

-----

#### 7. Start the Docker container

Put the script file in the /bin directory, and give the execution permission, and then directly execute the script file, so that Docker can start successfully.

```shell
# cp shell script to /bin
cp dockerd.sh /bin
# Modify file permissions
chmod 755 /bin/dockerd.sh
# start docker daemon.
dockerd.sh &
```

-----

### 

