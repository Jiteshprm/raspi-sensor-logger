# raspi-sensor-logger

    cd raspi-sensor-logger
    chmod +x install.sh
    sudo ./install.sh

   
    sqlite3 /mnt/ramdisk/mqtt_ramdisk.db

    birdofprey@birdofprey-rasp-desktop:~/raspi-sensor-logger$ sqlite3 /mnt/ramdisk/mqtt_ramdisk.db
    SQLite version 3.11.0 2016-02-15 17:29:24
    Enter ".help" for usage hints.
    sqlite> .tables
    bh1750_lux    bme280_hum    bme280_pres   bme280_temp   ds18s20_temp
    sqlite> 
