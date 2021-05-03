## 跨架构迁移

跨架构迁移指的是将X86架构的Ubuntu中的容器迁移到ARM架构的安卓操作系统中运行，迁移后的容器拥有容器迁移时的状态。

迁移到安卓需要和后端服务程序结合使用，因为后端服务程序中有转换CRIU镜像文件的脚本。

本功能需要用到[criu-het](https://github.com/systems-nuts/criu-het),是一个支持跨架构迁移的CRIU工具，对CRIU进行了修改，版本为3.11。

跨架构迁移需要定制的docker镜像才能正常工作，使用了[h-container](https://github.com/systems-nuts/hcontainer-tutorial)

Ubuntu的版本为18.04.1，内核版本为4.15。

#### 在Ubuntu操作系统中安装criu-het

1.安装依赖环境

```shell
sudo apt-get update
sudo apt-get install -y protobuf-c-compiler libprotobuf-c-dev gcc build-essential bsdmainutils python git-core asciidoc make htop curl supervisor cgroup-lite libapparmor-dev libseccomp-dev libprotobuf-dev libaio-dev apparmor libnet1-dev protobuf-compiler python-protobuf libnl-3-dev libcap-dev python-dev  build-essential libssl-dev libffi-dev  libxml2-dev libxslt1-dev zlib1g-dev
pip install ipaddress 
pip install pyfastcopy 
```

2.编译criu-het

```
git clone https://github.com/systems-nuts/criu-het.git
cd criu-het
git checkout heterogeneous-simplified
make
make install
```

3. 安装Docker

```shell
wget https://download.docker.com/linux/static/stable/x86_64/docker-19.03.6.tgz
tar xvf docker-19.03.6.tgz
cd docker
sudo cp ./* /usr/bin
```

4. 运行Docker守护进程

```shell
sudo su
dockerd &
```

### 

### 安卓相关

##### 1. criu和tar

* 因为要进行跨架构迁移，所以首先要用到CRIU，如何移植CRIU在本仓库的另一个文件夹中。

* 除了移植CRIU之外，还需要使用新版本的tar工具，才能够使得容器的checkpoint能够成功。

* 这里我们使用静态的二进制文件，已经放在了仓库中，将该tar文件复制到/bin目录下，然后赋予可执行的权限。

* 仓库中的build-tar-static.sh为编译tar工具的脚本，需要使用ARM架构的ubuntu进行编译。

##### 2. 内存布局

跨架构迁移需要和ubuntu统一地址布局，ubuntu中使用48位分配地址空间，安卓默认是39位，因此需要修改内核，添加`CONFIG_ARM64_VA_BITS_48=y`编译选项

然后修改一个源代码文件，注释掉其中两行代码

```
//static inline void mm_inc_nr_puds(struct mm_struct *mm) {}
//static inline void mm_dec_nr_puds(struct mm_struct *mm) {}
```

最后再编译你的内核，就拥有了和ubuntu统一的内存地址空间，这样就能够进行跨架构容器迁移了。

## 演示案例

