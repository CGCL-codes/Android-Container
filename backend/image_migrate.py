import hashlib
import json
import os
import sys
import uuid
import time

import docker

# 获取docker client
client = docker.from_env()


def logs(args):
    print(args)
    pass


# 获取文件的sha256sum
def get_file_sha256(filename):
    # 如果不是文件，返回空
    if not os.path.isfile(filename):
        return
    hash_sum = hashlib.sha256()
    f = open(filename, 'rb')
    hash_sum.update(f.read())
    f.close()
    return hash_sum.hexdigest()


# 解压文件
def unpack(filename):
    if not os.path.isfile(filename):
        return
    tmp_dir = '/tmp/' + str(uuid.uuid4())
    os.system(f'mkdir {tmp_dir}')
    os.system(f'tar -xf {filename} -C {tmp_dir}')
    return tmp_dir + '/'


def get_tar(container_id, filename, repository="migrate", tag="test"):
    image_id = client.containers.get(container_id).commit(repository=repository,tag=tag).id.replace("sha256:", "")
    save_dir = "/tmp/" + filename
    os.system(f'docker  save -o {save_dir} {image_id} {repository}:{tag}')
    # 去除换行符再返回
    return image_id, save_dir


def qemu_arm_start():
    client.containers.run('multiarch/qemu-user-static:register', privileged=True, remove=True)


def start_arm_container(images_name):
    _out = client.containers.run(f'arm64v8/{images_name}', detach=True, name='arm64_tmp')
    os.system('echo "x86 to arm64" > /tmp/.image_to_arm')
    os.system('docker cp /tmp/.image_to_arm arm64_tmp:/root/')
    return _out.id


def get_image_name(container_id):
    image_name = client.containers.get(container_id).attrs['Config']['Image']
    if ':' in image_name:
        return image_name
    return image_name + ':latest'


def get_target_tar(container_id, repository="migrate", tag="test"):
    x86_get_time_start = time.time()
    logs(f'获取x86架构的镜像文件中...')
    x86_image_id, x86_file = get_tar(container_id, 'x86.tar')
    x86_get_time_end = time.time()
    logs(f'获取到镜像的tar文件，文件名：{x86_file}，耗时：{x86_get_time_end - x86_get_time_start}')
    x86_unpack_time_start = time.time()
    logs(f'解压镜像文件中...')
    x86_save_dir = unpack(x86_file)
    x86_unpack_time_end = time.time()
    logs(f'解压完成，耗时：{x86_unpack_time_end - x86_unpack_time_start}')
    arm_time_start = time.time()
    logs(f'启动ARM容器中...')
    qemu_arm_start()
    image_name = get_image_name(container_id)
    start_arm_container(image_name)
    arm_time_end = time.time()
    logs(f'容器启动完成，耗时：{arm_time_end - arm_time_start}')
    arm_get_time_start = time.time()
    logs(f'获取arm架构的镜像文件中...')
    arm_image_id, arm_file = get_tar('arm64_tmp', 'arm64.tar', repository, tag)
    arm_get_time_end = time.time()
    logs(f'获取到arm镜像的tar文件，文件名：{arm_file}，耗时：{arm_get_time_end - arm_get_time_start}')
    arm_unpack_time_start = time.time()
    logs(f'解压arm镜像文件中...')
    arm_save_dir = unpack(arm_file)
    arm_unpack_time_end = time.time()
    logs(f'解压完成，耗时：{arm_unpack_time_end - arm_unpack_time_start}')
    config_time_start = time.time()
    logs(f'重写配置文件中...')
    x86_tar_sha256sum, x86_file_path, x86_json = get_top_layer(x86_save_dir, 'manifest.json')
    arm_tar_sha256sum, arm_file_path, arm_json = get_top_layer(arm_save_dir, 'manifest.json')
    # 复制镜像层文件
    os.system(f'cp {x86_save_dir}{x86_file_path} {arm_save_dir}{arm_file_path}')
    # 修改文件对应的sha256的值
    if sys.platform == 'darwin':
        os.system(f'sed -i \'\' \'s/{arm_tar_sha256sum}/{x86_tar_sha256sum}/g\' {arm_save_dir}{arm_json}')
    elif sys.platform == 'linux':
        os.system(f'sed -i \'s/{arm_tar_sha256sum}/{x86_tar_sha256sum}/g\' {arm_save_dir}{arm_json}')
    config_time_end = time.time()
    logs(f'配置文件重写完成，耗时：{config_time_end - config_time_start}')
    pack_time_start = time.time()
    # 重新打包
    logs(f'重新打包中...')
    os.system(f'cd {arm_save_dir} && tar -zcf /tmp/arm64-target.tar.xz .')
    pack_time_end = time.time()
    logs(f'重新打包完成，耗时：{pack_time_end - pack_time_start}')
    logs('获取数据卷中...')
    volume_time_start = time.time()
    get_volume_tar(container_id)
    volume_time_end = time.time()
    logs(f'获取数据卷完成，耗时：{volume_time_end - volume_time_start}')
    rm_time_start = time.time()
    logs(f'删除临时文件中...')
    # 删除临时文件
    os.system(f'rm -rf {arm_save_dir} {x86_save_dir} /tmp/arm64.tar /tmp/x86.tar')
    # 删除镜像文件
    os.system(f'docker  rmi {x86_image_id} > /dev/null')
    os.system(f'docker  rmi {arm_image_id} > /dev/null')
    os.system(f'docker  rm -f arm64_tmp > /dev/null')
    rm_time_end = time.time()
    logs(f'临时文件删除完成...，耗时：{rm_time_end - rm_time_start}')
    logs(f'总共耗时：{rm_time_end - x86_get_time_start}')
    os.system("mv /tmp/arm64-target.tar.xz ~/migrate/html/images/")
    return '/tmp/arm64-target.tar.xz'


def get_tar_sha256sum(file_dir, filename):
    with open(file_dir + filename, 'r', encoding='utf8')as image:
        json_images = json.load(image)
        sha256sum = json_images['rootfs']['diff_ids'][-1]
    return sha256sum.split(':', 1)[1]


def get_top_layer(file_dir, filename):
    with open(file_dir+filename, 'r', encoding='utf8')as fp:
        json_manifest = json.load(fp)
        json_str = json_manifest[0]
        filename = json_str['Config']
        sha256sum = get_tar_sha256sum(file_dir, filename)
        layer = json_str['Layers'][-1]
        return sha256sum, layer, filename


def get_volume_tar(container_id):
    container = client.containers.get(container_id)
    mounts = container.attrs['Mounts']
    for mount in mounts:
        _data_dir = mount['Source']
        if '_data' in _data_dir:
            os.system(f'cd {_data_dir} && tar -czf /tmp/arm64-target-volume.tar.xz .')
    return '/tmp/arm64-target-volume.tar.xz'


if __name__ == '__main__':
    get_target_tar('4ee013c99ec1')

