#!/usr/bin/python

import json
import os
import pycriu

filepath = "/tmp/simple/"

mountfile = ""
IMG_files ={}

def getmountfile(filepath):
    files = os.listdir(filepath)
    for file in files:
        if "mountpoints" in file:
            return os.path.join(filepath,file)

# load img files
def load_image_file(file_path):
	###use a cache to avoid reloading the same file multiple times
	if file_path in IMG_files:
		return IMG_files[file_path]
		
	try:
		mnt_img = pycriu.images.load(open(file_path, 'rb'), pretty=True)
	except pycriu.images.MagicException as exc:
		print("Error reading", file_path)
		sys.exit(1)
	IMG_files[file_path] = mnt_img
	return mnt_img


def deleteMountpoint():
    mountfile = getmountfile(filepath)
    mnt_img = load_image_file(mountfile)
    # print(mnt_img["entries"])
    idx = 0
    for entry in mnt_img["entries"]:
        key = entry["mountpoint"]
        # print(key)
        if "systemd" in key:
            del mnt_img["entries"][idx]
        if "memory" in key:
            del mnt_img["entries"][idx]
        if "kcore" in key:
            del mnt_img["entries"][idx]
        if "/proc/acpi" in key:
            del mnt_img["entries"][idx]
        idx += 1
    pycriu.images.dump(mnt_img, open(mountfile, "w+"))


if __name__ == "__main__":
    # deleteMountpoint()
    out = os.popen("cd /tmp/simple && crit show mountpoints* | grep acpi")
    text = out.read()
    out.close()
    print(text)
    while "acpi" in text:
        deleteMountpoint()
        out = os.popen("cd /tmp/simple && crit show mountpoints* | grep acpi")
        text = out.read()
        out.close()
        
