#!/bin/bash

#rm -rf /mnt/ramdisk
#mkdir /mnt/ramdisk
#mount -osize=30m tmpfs /mnt/ramdisk -t tmpfs
#chmod 777 /mnt/ramdisk
#sqlite3 /mnt/ramdisk/mqtt_ramdisk.db "VACUUM;PRAGMA auto_vacuum = 1;"
#chown birdofprey:birdofprey /mnt/ramdisk/mqtt_ramdisk.db
#chmod -R 777 /mnt/ramdisk
#echo "Directory /mnt/ramdisk created."

function fail {
    sleep 2
    exit 1
}
python3 -u /opt/raspi-sensor-logger/ram_logger/ram_logger.py || fail