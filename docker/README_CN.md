## 安卓中运行容器

这些文件是Docker的静态二进制文件，版本为19.03.5。

安卓操作系统的版本为：安卓10，内核版本为4.14.180。

### 步骤

-----

#### 1. 编译内核源码

安卓系统默认对内核进行了裁剪，但是运行容器需要很多内核特性的支持，因此需要对内核进行编译。你的内核需要有以下一些内核配置选项：

|            内核配置选项             |         解释说明          |
| :---------------------------------: | :-----------------------: |
|          CONFIG_NAMESPACES          |         命名空间          |
|            CONFIG_NET_NS            |       网络命名空间        |
|            CONFIG_PID_NS            |        PID命名空间        |
|            CONFIG_IPC_NS            |        IPC命名空间        |
|            CONFIG_UTS_NS            |        UTS命名空间        |
|           CONFIG_CGROUPS            |       cgroup控制组        |
|        CONFIG_CGROUP_CPUACCT        |   cgroup的cpuacct子系统   |
|        CONFIG_CGROUP_DEVICE         |   cgroup的device子系统    |
|        CONFIG_CGROUP_FREEZER        |   cgroup的freezer子系统   |
|         CONFIG_CGROUP_SCHED         |    cgroup的sched子系统    |
|           CONFIG_CPUSETS            |   cgroup的cpuset子系统    |
|            CONFIG_MEMCG             |    cgroup的memcg子系统    |
|             CONFIG_KEYS             |     访问密钥保留支持      |
|             CONFIG_VETH             |     虚拟以太网对设备      |
|            CONFIG_BRIDGE            |     802.1d 以太网桥接     |
|       CONFIG_BRIDGE_NETFILTER       |   桥接IP/ARP数据包过滤    |
|         CONFIG_NF_NAT_IPV4          |     IPv4虚拟地址转换      |
|         CONFIG_IP_NF_FILTER         |       IP数据包过滤        |
|   CONFIG_IP_NF_TARGET_MASQUERADE    |    MASQUERADE目标支持     |
| CONFIG_NETFILTER_XT_MATCH_ADDRTYPE  | addrtype地址类型匹配支持  |
| CONFIG_NETFILTER_XT_MATCH_CONNTRACK | conntrack连接跟踪匹配支持 |
|   CONFIG_NETFILTER_XT_MATCH_IPVS    |       ipvs匹配支持        |
|          CONFIG_IP_NF_NAT           | iptables虚拟地址转换支持  |
|        CONFIG_NF_NAT_NEEDED         |     虚拟地址转换相关      |
|         CONFIG_POSIX_MQUEUE         |       POSIX消息队列       |
|          CONFIG_OVERLAY_FS          |    overlay文件系统支持    |
|             CONFIG_AIO              |      POSIX异步IO支持      |
|             CONFIG_TTY              |       启用字符终端        |

编译内核和添加内核编译选项的步骤：

```shell
# 进入内核源码根目录
cd /kenel/k20pro
# 使用指定的配置文件raphael_defconfig，配置文件在arch/x86/configs
make raphael_defconfig
# 使用图形化的方式添加内核编译选项，添加上面的一个个选项，可以使用"/"对应的按键搜索内核选项的位置
make menuconfig
# 编译内核
make -j4
```

-----

#### 2. 修改cpuset.c代码

由于安卓默认将cpuset子系统的前缀cpuset删除了，但是Docker需要这部分前缀，因此需要修改cgroup中的cpuset.c源代码，加上这部分前缀。文件的位置在：kernel/cgroup/cpuset.c，修改的内容为：

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

需要说明的是，修改的时候以上的内容从修改的文件中复制，然后加上`cpuset.`前缀。

------

#### 3. 下载Docker的二进制文件

当上面的都修改好了之后，就有了运行容器的内核特性支持，然后将Docker的静态二进制文件下载，然后全部复制到/bin目录下，并添加执行权限，便能够直接调用，[下载地址](https://download.docker.com/linux/static/stable/aarch64/)。

------

#### 4. 修改读写权限

由于目前使用了一些只读的文件目录，需要修改文件系统的读写权限。可以通过adb工具连接上手机，然后输入`adb remount`，将文件系统修改为可读可写。

-----

#### 5. 挂载所有的cgroup子系统

修改安卓操作系统的/etc/cgroup.json文件，修改为以下的内容，用于挂载所有的cgroup子系统。

```json
{"Cgroups":[{"UID":"system","GID":"system","Mode":"0755","Controller":"blkio","Path":"/dev/blkio"},{"UID":"system","GID":"system","Mode":"0755","Controller":"cpu","Path":"/dev/cpu"},{"Mode":"0555","Path":"/dev/cpuacct","Controller":"cpuacct"},{"UID":"system","GID":"system","Mode":"0755","Controller":"cpuset","Path":"/dev/cpuset"},{"UID":"system","GID":"system","Mode":"0755","Controller":"memory","Path":"/dev/memcg"},{"UID":"system","GID":"system","Mode":"0755","Controller":"schedtune","Path":"/dev/stune"},{"GID":"system","UID":"system","Mode":"0755","Controller":"devices","Path":"/dev/devices"},{"GID":"system","UID":"system","Mode":"0755","Controller":"freezer","Path":"/dev/freezer"},{"GID":"system","UID":"system","Mode":"0755","Controller":"hugetlb","Path":"/dev/hugetlb"},{"GID":"system","UID":"system","Mode":"0755","Controller":"net_cls","Path":"/dev/net_cls"},{"GID":"system","UID":"system","Mode":"0755","Controller":"net_prio","Path":"/dev/net_prio"},{"GID":"system","UID":"system","Mode":"0755","Controller":"perf_event","Path":"/dev/perf_event"},{"GID":"system","UID":"system","Mode":"0755","Controller":"pids","Path":"/dev/pids"},{"GID":"system","UID":"system","Mode":"0755","Controller":"rdma","Path":"/dev/rdma"}],"Cgroups2":{"UID":"root","GID":"root","Mode":"0600","Path":"/dev/cg2_bpf"}}
```

为了方便查看，对json数据进行格式化，如下：

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

-----

#### 6. 使用脚本启动Docker

Docker运行时需要一些文件目录， 安卓中默认没有这些文件目录，因此利用脚本文件来创建。并且由于缺少IP路由规则，需要添加两条规则。此外，还需要关闭SELinux，关闭了才能访问一些文件目录。

值得一提的是，为了使用crun容器运行时，需要挂载cgroup到/sys/fs/cgroup中，因此在脚本文件中添加这部分内容。脚本文件内容如下：

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

#### 7. 启动Docker容器

将脚本文件放到/bin目录下，并且赋予执行权限，然后直接执行该脚本文件，这样Docker就能成功启动了。

```shell
# cp shell script to /bin
cp dockerd.sh /bin
# Modify file permissions
chmod 755 /bin/dockerd.sh
# start docker daemon.
dockerd.sh &
```

-----

