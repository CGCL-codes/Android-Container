# Android-CRIU
To use criu on android platform.



By using docker-arm64/alpine image to build criu,and using patchelf to patch the criu.



## How to use

```bash
adb shell
cp -r criu /
chmod -R 777 criu
cd criu
./criu check
```

## how to compile

Use docker to compile.

```dockerfile
docker run --rm --privileged multiarch/qemu-user-static:register --reset

docker run -itd --name criu -v /usr/bin/qemu-aarch64-static:/usr/bin/qemu-aarch64-static arm64v8/alpine /bin/sh

docker exec -it criu sh

#go into container and download criu v3.13

#install compile tools

apk update && \
	sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
        apk add \
            tar \
            ip6tables \
            build-base \
            coreutils \
            git \
            protobuf-c-dev \
            protobuf-dev \
            python \
            libaio-dev \
            libcap-dev \
            libnl3-dev \
            pkgconfig \
            libnet-dev \
            ccache \
            gcc \
            iptables \
	    automake \
	    autoconf
      
#compile patchelf
git clone https://github.com/NixOS/patchelf && cd patchelf && ./bootstrap.sh && ./configure && make && make install

#compile criu
cd root && cd criu && make

#patch criu
for program in criu/criu; do \
        echo "Patching $program"; \
        patchelf --set-interpreter /criu/ld-linux-aarch64.so.1 --set-rpath /criu "$program" && \
        patchelf --replace-needed libc.ld-linux-aarch64.so.1 ld-linux-aarch64.so.1 "$program"; \
    done
    
#copy file to /criu
mkdir /criu && cd /criu
cp /root/criu/criu/criu /criu && cp /lib/ld-linux-aarch64.so.1 \
        /usr/lib/aarch64-linux-gnu/libprotobuf-c.so.1 \
        /lib/aarch64-linux-gnu/libdl.so.2 \
        /lib/aarch64-linux-gnu/libnl-3.so.200 \
        /usr/lib/aarch64-linux-gnu/libnet.so.1 \
        /lib/aarch64-linux-gnu/libc.so.6 \
        /lib/aarch64-linux-gnu/libpthread.so.0 \
        /criu
```

## Some errors
To solve some error, you need the patch.And you need to delete the -Werror in Makefile.
```shell
diff --git a/compel/arch/aarch64/src/lib/include/uapi/asm/sigframe.h b/compel/arch/aarch64/src/lib/include/uapi/asm/sigframe.h
index bff714cc..371ca8c7 100644
--- a/compel/arch/aarch64/src/lib/include/uapi/asm/sigframe.h
+++ b/compel/arch/aarch64/src/lib/include/uapi/asm/sigframe.h
@@ -1,7 +1,6 @@
 #ifndef UAPI_COMPEL_ASM_SIGFRAME_H__
 #define UAPI_COMPEL_ASM_SIGFRAME_H__
 
-#include <asm/sigcontext.h>
 #include <sys/ucontext.h>
 
 #include <stdint.h>
@@ -10,6 +9,20 @@
 
 #define FPSIMD_MAGIC                   0x46508001
 
+#ifndef __aarch64__
+struct _aarch64_ctx {
+       __u32 magic;
+       __u32 size;
+};
+
+struct fpsimd_context {
+       struct _aarch64_ctx head;
+       __u32 fpsr;
+       __u32 fpcr;
+       __uint128_t vregs[32];
+};
+#endif
+
 typedef struct fpsimd_context          fpu_state_t;
 
 struct aux_context {
diff --git a/criu/arch/aarch64/include/asm/restorer.h b/criu/arch/aarch64/include/asm/restorer.h
index 120fa8fb..9a24a8ee 100644
--- a/criu/arch/aarch64/include/asm/restorer.h
+++ b/criu/arch/aarch64/include/asm/restorer.h
@@ -1,7 +1,6 @@
 #ifndef __CR_ASM_RESTORER_H__
 #define __CR_ASM_RESTORER_H__
 
-#include <asm/sigcontext.h>
 #include <sys/ucontext.h>
 
 #include "asm/types.h"
```

To enable cross-achitecture container migrate, you need  to apply [#1271](https://github.com/checkpoint-restore/criu/pull/1271) to your criu source.