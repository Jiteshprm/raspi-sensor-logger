#https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python/
import paho.mqtt.client as mqtt
import sqlite3
import time
import datetime

DATABASE_FILE = '/mnt/ramdisk/mqtt_ramdisk.db'
DATABASE_FILE_PERSISTENT = '/home/birdofprey/sensor_data.db'


def current_milli_time():
    return round(time.time() * 1000)


def current_milli_time_to_human(millisecs_since_epoch):
    return datetime.datetime.fromtimestamp(float(millisecs_since_epoch)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')


def print_with_msg_timestamp(msg):
    print ("[" + current_milli_time_to_human(current_milli_time()) + "]: " + msg)


def main():
    print ("main - Starting")
    print_with_msg_timestamp ("-----------------START------------------")
    db_conn = sqlite3.connect(DATABASE_FILE_PERSISTENT)
    sql = """
    ATTACH DATABASE '%s' AS mqtt_ramdisk;
    """ % DATABASE_FILE
    cursor = db_conn.cursor()
    print_with_msg_timestamp ("main - Executing: " + sql)
    cursor.execute(sql)

    sql = """
    SELECT name FROM mqtt_ramdisk.sqlite_master WHERE type='table';
    """
    cursor = db_conn.cursor()
    print_with_msg_timestamp ("main - Executing: " + sql)
    cursor.execute(sql)
    alltables = cursor.fetchall()
    print_with_msg_timestamp ("main - found %s tables: " % len(alltables))
    for t in alltables:
        t_name = t[0]
        print_with_msg_timestamp ("main - Copying table: " + t_name)
        sql = """
            CREATE TABLE IF NOT EXISTS main.%s (
            timestamp_sensor_raw INTEGER PRIMARY KEY NOT NULL,
            timestamp_sensor_str TEXT NOT NULL,
            timestamp_msg_raw INTEGER NOT NULL,
            timestamp_msg_str TEXT NOT NULL,        
            value_raw INTEGER NOT NULL,
            value_str TEXT NOT NULL);
        """ % t_name
        cursor = db_conn.cursor()
        print_with_msg_timestamp ("main - Executing: " + sql)
        cursor.execute(sql)
        sql = """
            insert or ignore into main.%s select * from mqtt_ramdisk.%s;
            """ % (t_name, t_name)
        cursor = db_conn.cursor()
        print_with_msg_timestamp ("main - Executing: " + sql)
        cursor.execute(sql)
        db_conn.commit()
    cursor.close()
    print_with_msg_timestamp ("-----------------FINISH------------------")

main()