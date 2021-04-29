#!/usr/bin/python3 -u
#https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python/
import os
import paho.mqtt.client as mqtt
import sqlite3
import time
from datetime import datetime, timedelta
import threading
import logging
import sys
import traceback

MQTT_HOST = '192.168.1.36'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'MQTT SqlLite3 Ram Logger'
MQTT_USER = 'YOUR MQTT USER'
MQTT_PASSWORD = 'YOUR MQTT USER PASSWORD'
TOPIC = 'sensors/#'

DATABASE_FILE = '/mnt/ramdisk/mqtt_ramdisk.db'

table_name_cache = {""}
timestamp_msg = 0
next_call = time.time()
time_to_cleanup = False


def current_milli_time():
    return round(time.time() * 1000)


def current_milli_time_to_human(millisecs_since_epoch):
    return datetime.fromtimestamp(float(millisecs_since_epoch)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')


def print_with_msg_timestamp(msg):
    print ("[" + current_milli_time_to_human(timestamp_msg) + "]: " + msg)


#https://stackoverflow.com/questions/4415672/python-theading-timer-how-to-pass-argument-to-the-callback
#https://stackoverflow.com/questions/8600161/executing-periodic-actions
#https://stackoverflow.com/questions/46402022/subtract-hours-and-minutes-from-time
#https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime
def cleanup_timer():
    print_with_msg_timestamp("========cleanup_timer - Started==========")
    global time_to_cleanup
    time_to_cleanup = True
    global next_call
    next_call = next_call+86400/4 #1 day
    print_with_msg_timestamp("cleanup_timer - Next call @ " + current_milli_time_to_human(next_call * 1000))
    threading.Timer(next_call - time.time(), cleanup_timer).start()
    print_with_msg_timestamp("========cleanup_timer - Finished========")


def execute_cleanup (db_conn):
    print_with_msg_timestamp("+++++++++++execute_cleanup - Started+++++++++++")
    global time_to_cleanup
    time_to_cleanup = False
    for table in table_name_cache:
        if len(table) > 0:
            timestamp_to_delete = datetime.today() - timedelta(days=1)
            timestamp_to_delete_from_epoch = round(timestamp_to_delete.timestamp()*1000)
            print_with_msg_timestamp("cleanup_timer - Found table to cleanup: " + table + " - TimeStamp to cutoff from: " + str(timestamp_to_delete.strftime('%Y-%m-%d %H:%M:%S.%f')) + " Timestamp from epoch: " + str(timestamp_to_delete_from_epoch))
            sql = 'DELETE FROM ' + table + ' WHERE timestamp_sensor_raw<' + str(timestamp_to_delete_from_epoch)
            print_with_msg_timestamp ("cleanup_timer - Executing Cleanup: " + sql)
            cursor = db_conn.cursor()
            cursor.execute(sql)
    print_with_msg_timestamp("+++++++++++execute_cleanup - Finished+++++++++++")


def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC,2)


def check_if_table_exists_in_cache(table_name):
    if table_name in table_name_cache:
        print_with_msg_timestamp ("check_if_table_exists_in_cache - Table_name:" + table_name + " in cache")
        return True
    else:
        print_with_msg_timestamp ("check_if_table_exists_in_cache - Table_name:" + table_name + " NOT in cache")
        return False


def check_if_table_exists_in_db(table_name, user_data):
    print_with_msg_timestamp ("check_if_table_exists_in_db - Table_name:" + table_name)
    table_exists_in_db = False
    db_conn = user_data['db_conn']
    sql = """
            SELECT name FROM sqlite_master WHERE type='table' and name='%s';
                        """ % table_name
    cursor = db_conn.cursor()
    print_with_msg_timestamp ("check_if_table_exists_in_db - Executing: " + sql)
    cursor.execute(sql)
    row_count = len(cursor.fetchall())
    print_with_msg_timestamp ("check_if_table_exists_in_db - Found Number of Tables: " + str(row_count))
    if row_count > 0:
        table_name_cache.add(table_name)
        table_exists_in_db = True
    cursor.close()
    return table_exists_in_db


def create_table_if_not_exists(table_name, user_data):
    print_with_msg_timestamp ("create_table_if_not_exists - table_name:" + table_name)
    db_conn = user_data['db_conn']
    sql = """
    CREATE TABLE IF NOT EXISTS """ + table_name + """ (
        timestamp_sensor_raw INTEGER PRIMARY KEY NOT NULL,
        timestamp_sensor_str TEXT NOT NULL,
        timestamp_msg_raw INTEGER NOT NULL,
        timestamp_msg_str TEXT NOT NULL,        
        value_raw INTEGER NOT NULL,
        value_str TEXT NOT NULL
    )
    """
    cursor = db_conn.cursor()
    print_with_msg_timestamp ("create_table_if_not_exists - Executing: " + sql)
    cursor.execute(sql)
    cursor.close()
    table_name_cache.add(table_name)


def check_if_table_exists_or_else_create(table_name, user_data):
    if not check_if_table_exists_in_cache(table_name):
        if not check_if_table_exists_in_db(table_name, user_data):
            create_table_if_not_exists(table_name, user_data)


def on_message(mqtt_client, user_data, message):
        global timestamp_msg
        timestamp_msg = current_milli_time()
        print_with_msg_timestamp ("-----------------START------------------")
        print_with_msg_timestamp ("on_message - received message: " + str(message.payload) + " topic: " + str(message.topic))
        payload = message.payload.decode('utf-8')
        table_name = message.topic.split("/")[1]
        print_with_msg_timestamp ("on_message - table_name:" + table_name)
        check_if_table_exists_or_else_create(table_name, user_data)
        if ("cleanup" in payload):
            payload_processed = payload.split("|")
            timestamp_to_delete = payload_processed[1]
            sql = 'DELETE FROM ' + table_name + ' WHERE timestamp_sensor_raw<' + timestamp_to_delete
            cursor = db_conn.cursor()
            print_with_msg_timestamp ("on_message - Executing Cleanup: " + sql)
            cursor.execute(sql)
        else:
            db_conn = user_data['db_conn']
            sql = 'INSERT INTO ' + table_name + '(timestamp_sensor_raw, timestamp_sensor_str, timestamp_msg_raw, timestamp_msg_str, value_raw, value_str) VALUES (?, ?, ?, ?, ?, ?)'
            cursor = db_conn.cursor()
            payload_processed = payload.split("|")
            timestamp_sensor_raw = payload_processed[0]
            timestamp_sensor_str = current_milli_time_to_human(timestamp_sensor_raw)
            value_raw = payload_processed[1]
            value_str = payload_processed[2]
            timestamp_msg_raw = timestamp_msg
            timestamp_msg_str = current_milli_time_to_human(timestamp_msg_raw)
            print_with_msg_timestamp ("on_message - Executing: " + sql + " (%s, %s, %s, %s, %s, %s)" % (timestamp_sensor_raw, timestamp_sensor_str, timestamp_msg_raw, timestamp_msg_str, value_raw, value_str))
            cursor.execute(sql, (timestamp_sensor_raw, timestamp_sensor_str, timestamp_msg_raw, timestamp_msg_str, value_raw, value_str))
        db_conn.commit()
        cursor.close()
        print_with_msg_timestamp ("on_message - Finished processing message")
        print_with_msg_timestamp ("-----------------FINISH------------------")
        global time_to_cleanup
        if time_to_cleanup:
            execute_cleanup(db_conn)
        print_with_msg_timestamp ("on_message - Waiting for next message...")


def handle_excepthook(type, message, stack):
    print_with_msg_timestamp("An unhandled exception occured:" + str(message) + ". Traceback: " + repr(traceback.format_tb(stack)))
    #+
    time.sleep(1)
    os._exit(1)


def main():
    print ("main - Starting")
    db_conn = sqlite3.connect(DATABASE_FILE)

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    #mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    cleanup_timer()

    sys.excepthook = handle_excepthook

    print ("main - Waiting for Messages...")
    mqtt_client.loop_forever()


main()