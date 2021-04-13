#/bin/bash

sudo mkdir /mnt/ramdisk
sudo mount -osize=10m tmpfs /mnt/ramdisk -t tmpfs
python ram_logger.py