# Android Container
**English** | [中文](README_CN.md)

This project is used to run Linux containers in Android, such as Docker, Podman, etc. And it can migrate X86-based containers to the Android system to achieve cross-architecture container migration. The project needs to compile the Android source code and modify the kernel source code, so you need to understand AOSP compilation. You can use this project to run a complete container in the Android operating system and be able to use normal container functions.

-----

This project uses the Android smartphone Redmi K20 Pro as the experimental device.

## Project Directory

```
├── CoClient # Android client, used to manage containers in Android
│
├── README.md
├── README_CN.md
├── backend # Cross-architecture migration backend service program
│ ├── README.md
│ ├── README_EN.md
│ ├── backend.py
│ ├── container_migrate.py
│ ├── docker-popcorn-notify
│ ├── image_migrate.py
│ ├── mnt.py
│ └── recode.sh
├── criu # Use criu module in Android
│
├── docker # Run Docker container in Android
│ ├── README.md
│ ├── README_CN.md
│ ├── containerd
│ ├── containerd-shim
│ ├── ctr
│ ├── docker
│ ├── docker-init
│ ├── docker-proxy
│ ├── dockerd
│ └── runc
├── files # Android total cgroup configuration file and docker startup script
│ ├── cgroups.json
│ └── dockerd.sh
├── migration # Cross-architecture migration related
│ ├── README.md
│ ├── README_CN.md
│ ├── build-tar-static.sh
│ └── tar
└── picture # effect picture
    ├── 1.png
    └── 2.png
```

### Effect

The rendering of the container running in Android.

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

