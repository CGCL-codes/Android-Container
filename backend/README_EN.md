## 后端

后端服务程序模块，用于实现跨架构迁移容器。将容器从ubuntu操作系统迁移到Android操作系统，迁移后的容器拥有容器迁移时的状态。

包含了跨架构迁移需要的转换模块，用于转换CRIU镜像文件，转换后的CRIU镜像文件才能在安卓操作系统中使用。

#### 如何使用

首先需要安装相关依赖

```shell
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install flask
pip3 install docker
```

根据你自己的IP地址修改backend.py中的IP，然后终端直接执行：

```shell
python3 backend.py
```

