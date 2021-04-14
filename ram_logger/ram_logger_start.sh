#/bin/bash

sudo mkdir /mnt/ramdisk
sudo mount -osize=10m tmpfs /mnt/ramdisk -t tmpfs
python3 ram_logger.py