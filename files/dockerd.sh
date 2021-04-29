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

#if [ ! -d "/dev/freezer" ]; then
        #mkdir /dev/blkio
        #mkdir /dev/cpu
        #mkdir /dev/cpuacct
        #mkdir /dev/cpuset
        #mkdir /dev/devices
        #mkdir /dev/freezer
        #mkdir /dev/hugetlb
        #mkdir /dev/memory
        #mkdir /dev/net_cls
        #mkdir /dev/net_prio
        #mkdir /dev/perf_event
        #mkdir /dev/pids
        #mkdir /dev/rdma
        #mkdir /dev/stune
#fi

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


# mount cgroup
#mount -t cgroup -o blkio none /dev/blkio
#mount -t cgroup -o cpu none /dev/cpu
#mount -t cgroup -o cpuacct none /dev/cpuacct
#mount -t cgroup -o cpuset none /dev/cpuset
#mount -t cgroup -o devices none /dev/devices
#mount -t cgroup -o freezer none /dev/freezer
#mount -t cgroup -o hugetlb none /dev/hugetlb
#mount -t cgroup -o memory none /dev/memory
#mount -t cgroup -o net_cls none /dev/net_cls
#mount -t cgroup -o net_prio none /dev/net_prio
#mount -t cgroup -o perf_event none /dev/perf_event
#mount -t cgroup -o pids none /dev/pids
#mount -t cgroup -o rdma none /dev/rdma
#mount -t cgroup -o schedtune none /dev/stune

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
#modprobe br_netfilter
setenforce 0
# run dockerd
export DOCKER_RAMDISK=true
#dockerd --add-runtime crun=/bin/crun -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock > /dev/null 2>&1 &
dockerd --add-runtime crun=/bin/crun -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock &
