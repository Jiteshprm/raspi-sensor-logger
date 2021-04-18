# raspi-sensor-logger

    cd raspi-sensor-logger
    chmod +x install.sh
    sudo ./install.sh

   
    sqlite3 /mnt/ramdisk/mqtt_ramdisk.db
    sqlite3 /home/birdofprey/sensor_data.db
    ls -larth  /mnt/ramdisk/mqtt_ramdisk.db
    ls -larth  /home/birdofprey/sensor_data.db
    birdofprey@birdofprey-rasp-desktop:~/raspi-sensor-logger$ sqlite3 /mnt/ramdisk/mqtt_ramdisk.db
    SQLite version 3.11.0 2016-02-15 17:29:24
    Enter ".help" for usage hints.
    sqlite> .tables
    bh1750_lux    bme280_hum    bme280_pres   bme280_temp   ds18s20_temp
    sqlite> 
    select * from bh1750_lux;
    select * from bme280_hum;
    select * from bme280_pres;
    select * from bme280_temp;
    select * from ds18s20_temp;
    
    delete from bh1750_lux where timestamp_sensor_raw<1618617597302;
    delete from bme280_hum where timestamp_sensor_raw<1618617597302;
    delete from bme280_pres where timestamp_sensor_raw<1618617597302;
    delete from bme280_temp where timestamp_sensor_raw<1618617597302;
    delete from ds18s20_temp where timestamp_sensor_raw<1618617597302;
    
    
    
    Enable auto vacuum:
    https://www.sqlite.org/pragma.html#pragma_auto_vacuum
    https://stackoverflow.com/questions/60409960/peewee-sqlite-auto-vacuum
    birdofprey@birdofprey-rasp-desktop:~/raspi-sensor-logger$ sqlite3 /mnt/ramdisk/mqtt_ramdisk.db
    SQLite version 3.11.0 2016-02-15 17:29:24
    Enter ".help" for usage hints.
    sqlite> PRAGMA auto_vacuum;
    0
    sqlite> PRAGMA auto_vacuum = 1;
    sqlite> PRAGMA auto_vacuum;
    0
    sqlite> PRAGMA auto_vacuum = 1;
    sqlite> VACUUM;
    sqlite> PRAGMA auto_vacuum = 1;
    sqlite> PRAGMA auto_vacuum;
    1

    
    
    sudo sh /opt/raspi-sensor-logger/stop_all_loggers.sh 
    git reset --hard
    git fetch;git pull
    chmod +x install.sh
    sudo ./install.sh
    
    sudo sh /opt/raspi-sensor-logger/start_all_loggers.sh
    
    sudo journalctl -f -u ds18s20
    sudo journalctl -f -u bme280 
    sudo journalctl -f -u bh1750 
    sudo journalctl -f -u persistent_logger 
    sudo journalctl -f -u ram_logger 
    
