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
    select * from accuweather_upper_holloway;
    
    select * from outdoor_bh1750_lux;
    select * from outdoor_bme280_alt;
    select * from outdoor_bme280_hum;
    select * from outdoor_bme280_pres;
    select * from outdoor_bme280_temp;
    select * from outdoor_sht31d_hum;
    select * from outdoor_sht31d_temp;
    select * from outdoor_accel;
    select * from outdoor_gyro;
    select * from outdoor_mag;
    select * from outdoor_uv;
    select * from outdoor_wifi_signal;
    select * from outdoor_memory;
    select * from outdoor_crash;
    select * from outdoor_restart;
    
    delete from bh1750_lux where timestamp_sensor_raw<1619046010000;
    delete from bme280_hum where timestamp_sensor_raw<1619046010000;
    delete from bme280_pres where timestamp_sensor_raw<1619046010000;
    delete from bme280_temp where timestamp_sensor_raw<1619046010000;
    delete from ds18s20_temp where timestamp_sensor_raw<1619046010000;
        delete from outdoor_bh1750_lux where timestamp_sensor_raw<1619046010000;
        delete from outdoor_bme280_alt where timestamp_sensor_raw<1619046010000;
        delete from outdoor_bme280_hum where timestamp_sensor_raw<1619046010000;
        delete from outdoor_bme280_pres where timestamp_sensor_raw<1619046010000;
        delete from outdoor_bme280_temp where timestamp_sensor_raw<1619046010000;
        delete from outdoor_sht31d_hum where timestamp_sensor_raw<1619046010000;
        delete from outdoor_sht31d_temp where timestamp_sensor_raw<1619046010000;
    
    delete from outdoor_accel where timestamp_sensor_raw>0;
    delete from outdoor_gyro where timestamp_sensor_raw>0;
    delete from outdoor_mag where timestamp_sensor_raw>0;
    delete from outdoor_uv where timestamp_sensor_raw>0;
    
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

    cd
    cd raspi-sensor-logger/
    sudo cp /opt/raspi-sensor-logger/accuweather/accuweather.py /tmp
    sudo sh /opt/raspi-sensor-logger/stop_all_loggers.sh 
    git reset --hard
    git fetch;git pull
    chmod +x install.sh
    sudo cp /tmp/accuweather.py accuweather/accuweather.py
    sudo ./install.sh
    
    sudo systemctl stop accuweather.service
    sudo vi /opt/raspi-sensor-logger/accuweather/accuweather.py
    sudo systemctl start accuweather.service
    
    sudo sh /opt/raspi-sensor-logger/start_all_loggers.sh
    
    sudo journalctl -f -u ds18s20
    sudo journalctl -f -u bme280 
    sudo journalctl -f -u bh1750 
    sudo journalctl -f -u persistent_logger 
    sudo journalctl -f -u ram_logger 
    sudo journalctl -f -u accuweather
    sudo journalctl -f -u ram_logger_create_folder
    sudo journalctl -f -u esp_update_delete.service
    
    sudo sh /opt/raspi-sensor-logger/stop_all_loggers.sh
    cp /mnt/ramdisk/mqtt_ramdisk.db /home/birdofprey    
    sudo umount /mnt/ramdisk    
    sudo mount -osize=30m tmpfs /mnt/ramdisk -t tmpfs
    chmod 777 /mnt/ramdisk
    cp /home/birdofprey/mqtt_ramdisk.db /mnt/ramdisk
    
    screen /dev/cu.usbserial 115200
    
    
    mosquitto_pub -h localhost -t sensors/outdoor_bme280_temp -m ""
    mosquitto_sub -h 127.0.0.1 -v -t sensors/#
----Enable Mosquitto Raspberry---
sudo service  mosquitto stop
sudo systemctl enable mosquitto
sudo service  mosquitto status
sudo service mosquitto start 
-----------------------------------
sudo less /var/log/mosquitto/mosquitto.log

1620475927: New client connected from 192.168.1.99:63471 as ESP8266Client-69a3 (p2, c1, k15).
1620475927: Client ESP8266Client-69a3 disconnected due to malformed packet.
1620475933: New connection from 192.168.1.99:51683 on port 1883.
1620475933: New client connected from 192.168.1.99:51683 as ESP8266Client-669d (p2, c1, k15).
1620475933: Client ESP8266Client-669d disconnected due to malformed packet.
1620475934: Client MQTT BH1750 Light Meter closed its connection.

sudo tcpdump -i enxb827eb6de4f7 -nn -s0 -X -v port 1883 and host 192.168.1.36 -w test.pcap
sudo tcpdump -i enxb827eb6de4f7 -nn -s0 -v port 21