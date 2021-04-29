# 安卓容器

这个项目用于在安卓系统中运行Linux容器，比如Docker、Podman等。并且能够将X86架构的容器迁移到安卓系统中，实现跨架构容器迁移。项目需要编译安卓源码、修改内核源码，因此你需要对AOSP的编译有所了解。你可以使用该项目在安卓操作系统中运行一个完整的容器，能够使用正常的容器功能。

------

本项目使用安卓智能手机Redmi K20 Pro作为实验设备。

### 效果

Android中运行容器的效果图。

<table>
  <tr>
    <td>Docker info</td>
     <td>hello-world container and criu</td>
  </tr>
  <tr>
    <td><img src="picture/1.png" width="460" height="995" alt="图片1"/></td>
    <td><img src="picture/2.png" width="460" height="995" alt="图片2"/></td>
  </tr>
 </table>
