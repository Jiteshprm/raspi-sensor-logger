#/bin/bash
#Must be run as sudo
if [ $EUID -ne 0 ]
  then echo "Please run with sudo!"
  exit
fi

set -x
systemctl daemon-reload
systemctl enable ram_logger_create_folder.service
systemctl start ram_logger_create_folder.service
sleep 1s
systemctl enable ram_logger.service
systemctl start ram_logger.service
sleep 1s
systemctl enable bh1750.service
systemctl start bh1750.service
sleep 5s
systemctl enable bme280.service
systemctl start bme280.service
sleep 5s
systemctl enable ds18s20.service
systemctl start ds18s20.service
systemctl enable persistent_logger.service
systemctl start persistent_logger.service
systemctl enable --now persistent_logger.timer
systemctl enable accuweather.service
systemctl enable --now accuweather.timer
systemctl start accuweather.service
systemctl enable esp_update_delete.service
systemctl start esp_update_delete.service

systemctl status ram_logger.service
systemctl status bme280.service
systemctl status ds18s20.service
systemctl status bh1750.service
systemctl status persistent_logger.service
systemctl status accuweather.service
systemctl status accuweather.service
systemctl status esp_update_delete.service
