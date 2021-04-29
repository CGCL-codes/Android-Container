## Cross-architecture migration

**English** | [中文](README_CN.md)

Cross-architecture migration refers to the migration of containers in the Ubuntu X86 architecture to the Android operating system of the ARM architecture, and the migrated containers have the state of the container at the time of migration.

Migrating to Android needs to be used in conjunction with the back-end service program, because there is a script to convert the CRIU image file in the back-end service program.

This function needs to use [criu-het](https://github.com/systems-nuts/criu-het), which is a CRIU tool that supports cross-architecture migration. CRIU has been modified and the version is 3.11.

Cross-architecture migration requires a customized docker image to work properly, using [h-container](https://github.com/systems-nuts/hcontainer-tutorial)

The Ubuntu version is 18.04.1 and the kernel version is 4.15.

#### Install criu-het in Ubuntu operating system

1. Installation dependent environment

```shell
sudo apt-get update
sudo apt-get install -y protobuf-c-compiler libprotobuf-c-dev gcc build-essential bsdmainutils python git-core asciidoc make htop curl supervisor cgroup-lite libapparmor-dev libseccomp-dev libprotobuf-dev libaio-dev apparmor libnet1-dev protobuf-compiler python-protobuf libnl-3-dev libcap-dev python-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
pip install ipaddress
pip install pyfastcopy
```

2. Compile criu-het

```
git clone https://github.com/systems-nuts/criu-het.git
cd criu-het
git checkout heterogeneous-simplified
make
make install
```

### Android related

##### 1. criu and tar

* Because of the cross-architecture migration, CRIU must be used first. How to migrate CRIU to another folder in this warehouse.

* In addition to transplanting CRIU, you also need to use a new version of the tar tool to make the container checkpoint successful.

* Here we use a static binary file, which has been placed in the warehouse, copy the tar file to the /bin directory, and then grant executable permissions.

* The build-tar-static.sh in the warehouse is the script for compiling the tar tool, which needs to be compiled with ubuntu of the ARM architecture.

##### 2. Memory layout

Cross-architecture migration needs to unify the address layout with ubuntu. In ubuntu, 48 bits are used to allocate the address space. Android defaults to 39 bits. Therefore, you need to modify the kernel and add the `CONFIG_ARM64_VA_BITS_48=y` compilation option.

Then modify a source code file, comment out two lines of code

```
//static inline void mm_inc_nr_puds(struct mm_struct *mm) {}
//static inline void mm_dec_nr_puds(struct mm_struct *mm) {}
```

Finally, compile your kernel, and you will have a unified memory address space with ubuntu, so that you can migrate across architecture containers.