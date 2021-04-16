#/bin/bash
#Must be run as sudo
echo $EUID
if [ "$EUID" -ne 0 ]
  then echo "Please run with sudo!"
  exit
fi

set -x
cp -r ../raspi-sensor-logger /opt
rm -rf /opt/raspi-sensor-logger/.git
find /opt/raspi-sensor-logger/ -type f -iname "*.sh" -exec chmod u+x {} \;
find /opt/raspi-sensor-logger/ -type f -iname "*.py" -exec chmod u+x {} \;

if [ -d "/mnt/ramdisk" ]
then
    echo "Directory /mnt/ramdisk exists."
else
    mkdir /mnt/ramdisk
    mount -osize=10m tmpfs /mnt/ramdisk -t tmpfs
    chmod 777 /mnt/ramdisk
fi

cp /opt/raspi-sensor-logger/services/* /etc/systemd/system
systemctl daemon-reload
systemctl enable ram_logger.service
systemctl start ram_logger.service

systemctl enable bh1750.service
systemctl start bh1750.service
systemctl enable bme280.service
systemctl start bme280.service
systemctl enable ds18s20.service
systemctl start ds18s20.service
systemctl enable persistent_logger.service
systemctl start persistent_logger.service


systemctl status ram_logger.service
systemctl status bme280.service
systemctl status ds18s20.service
systemctl status bh1750.service
systemctl status persistent_logger.service




