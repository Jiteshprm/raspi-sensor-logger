#!/bin/sh

rm -rf /mnt/ramdisk
mkdir /mnt/ramdisk
mount -osize=30m tmpfs /mnt/ramdisk -t tmpfs
chmod 777 /mnt/ramdisk
sqlite3 /mnt/ramdisk/mqtt_ramdisk.db "VACUUM;PRAGMA auto_vacuum = 1;"
chown birdofprey:birdofprey /mnt/ramdisk/mqtt_ramdisk.db
chmod -R 777 /mnt/ramdisk
echo "Directory /mnt/ramdisk created."
