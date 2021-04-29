#!/bin/bash
#
# build static tar because we need exercises in minimalism
# MIT licentar: google it or see robxu9.mit-license.org.
#
# For Linux, also builds musl for truly static linking.

tar_version="1.29"
musl_version="1.1.15"

platform=$(uname -s)

if [ -d build ]; then
  echo "= removing previous build directory"
  rm -rf build
fi

mkdir build # make build directory
pushd build

# download tarballs
echo "= downloading tar"
curl -LO http://ftp.gnu.org/gnu/tar/tar-${tar_version}.tar.xz

echo "= extracting tar"
tar xJf tar-${tar_version}.tar.xz

if [ "$platform" = "Linux" ]; then
  echo "= downloading musl"
  curl -LO http://www.musl-libc.org/releases/musl-${musl_version}.tar.gz

  echo "= extracting musl"
  tar -xf musl-${musl_version}.tar.gz

  echo "= building musl"
  working_dir=$(pwd)

  install_dir=${working_dir}/musl-install

  pushd musl-${musl_version}
  env CFLAGS="$CFLAGS -Os -ffunction-sections -fdata-sections" LDFLAGS='-Wl,--gc-sections' ./configure --prefix=${install_dir}
  make install
  popd # musl-${musl-version}

  echo "= setting CC to musl-gcc"
  export CC=${working_dir}/musl-install/bin/musl-gcc
  export CFLAGS="-static"
else
  echo "= WARNING: your platform does not support static binaries."
  echo "= (This is mainly due to non-static libc availability.)"
fi

echo "= building tar"

pushd tar-${tar_version}
env FORCE_UNSAFE_CONFIGURE=1 CFLAGS="$CFLAGS -Os -ffunction-sections -fdata-sections" LDFLAGS='-Wl,--gc-sections' ./configure
make
popd # tar-${tar_version}

popd # build

if [ ! -d releases ]; then
  mkdir releases
fi

echo "= striptease"
strip -s -R .comment -R .gnu.version --strip-unneeded build/tar-${tar_version}/src/tar
echo "= compressing"
upx --ultra-brute build/tar-${tar_version}/src/tar
echo "= extracting tar binary"
cp build/tar-${tar_version}/src/tar releases
echo "= done"
