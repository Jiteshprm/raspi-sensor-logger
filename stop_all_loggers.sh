#/bin/bash
#Must be run as sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run with sudo!"
  exit
fi

set -x
systemctl stop ram_logger.service
systemctl stop bme280.service
systemctl stop ds18s20.service
systemctl stop bh1750.service
systemctl stop persistent_logger.service
systemctl stop accuweather.service
