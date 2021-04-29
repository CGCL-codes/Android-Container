import os
import docker

def start_nginx():
    os.system("docker rm -f migrate")
    os.system("mkdir ~/migrate")
    os.system("mkdir -p ~/migrate/html/checkpoints")
    os.system("mkdir -p ~/migrate/html/images")
    # ~/migrate/html是存储html的位置，资源也存在这个目录，方便读取
    os.system("docker run --name migrate -itd -p 8080:80 -v ~/migrate/html:/usr/share/nginx/html nginx")


# 获取checkpoint压缩文件
def migrate(container_id, checkpoint_name="simple"):
    os.system(f"./docker-popcorn-notify {container_id} aarch64")
    os.system(f"docker checkpoint create {container_id} {checkpoint_name}")
    os.system(f"./recode.sh {container_id} {checkpoint_name} aarch64")
    os.system("python mnt.py")
    out = os.popen("cd /tmp/simple && crit show mountpoints* | grep acpi")
    text = out.read()
    out.close()
    while "acpi" in text:
        deleteMountpoint()
        out = os.popen("cd /tmp/simple && crit show mountpoints* | grep acpi")
        text = out.read()
        out.close()
    os.system(f"cd /tmp && tar -czf {checkpoint_name}.tar.xz {checkpoint_name}")
    os.system(f"mv /tmp/{checkpoint_name}.tar.xz ~/migrate/html/checkpoints/")
    path = "checkpoints/" + checkpoint_name + ".tar.xz"
    os.system(f"rm -rf /tmp/{checkpoint_name}")
    os.system(f"docker logs {container_id}")
    return path


if __name__ == '__main__':
    start_nginx()
    os.system("docker rm -f migrate_test")
    os.system("docker run --cap-add all --name migrate_test -d 123toorc/hcontainer-helloworld:hcontainer")
    print(migrate("migrate_test"))
