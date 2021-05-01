#!/bin/sh

if [ -d "/mnt/ramdisk" ]
then
    echo "Directory /mnt/ramdisk exists."
else
    mkdir /mnt/ramdisk
    mount -osize=30m tmpfs /mnt/ramdisk -t tmpfs
    chmod 777 /mnt/ramdisk
    sqlite3 /mnt/ramdisk/mqtt_ramdisk.db "VACUUM;PRAGMA auto_vacuum = 1;"
fi
