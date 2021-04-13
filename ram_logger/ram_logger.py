#https://lindevs.com/save-mqtt-data-to-sqlite-database-using-python/
import paho.mqtt.client as mqtt
import sqlite3
import time
import datetime

MQTT_HOST = '192.168.1.36'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'MQTT SqlLite3 Ram Logger'
MQTT_USER = 'YOUR MQTT USER'
MQTT_PASSWORD = 'YOUR MQTT USER PASSWORD'
TOPIC = 'sensors/#'

DATABASE_FILE = '/mnt/ramdisk/mqtt_ramdisk.db'

table_name_cache = {}


def current_milli_time():
    return round(time.time() * 1000)


def current_milli_time_to_human(millisecs_since_epoch):
    return datetime.datetime.fromtimestamp(float(millisecs_since_epoch)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')


def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC)


def check_if_table_exists_in_cache(table_name):
    if table_name in table_name_cache:
        print ("check_if_table_exists_in_cache - Table_name:" + table_name + " in cache")
        return True
    else:
        print ("check_if_table_exists_in_cache - Table_name:" + table_name + " NOT in cache")
        return False


def check_if_table_exists_in_db(table_name, user_data):
    print ("check_if_table_exists_in_db - Table_name:" + table_name)
    table_exists_in_db = False
    db_conn = user_data['db_conn']
    sql = """
            SELECT name FROM sqlite_master WHERE type='table' and name='%s';
                        """ % table_name
    cursor = db_conn.cursor()
    print ("check_if_table_exists_in_db - Executing: " + sql)
    cursor.execute(sql)
    row_count = len(cursor.fetchall())
    print ("check_if_table_exists_in_db - Found Number of Tables: " + str(row_count))
    if row_count > 0:
        table_exists_in_db = True
    cursor.close()
    return table_exists_in_db


def create_table_if_not_exists(table_name, user_data):
    print ("create_table_if_not_exists - table_name:" + table_name)
    db_conn = user_data['db_conn']
    sql = """
    CREATE TABLE IF NOT EXISTS """ + table_name + """ (
        timestamp_raw INTEGER PRIMARY KEY NOT NULL,
        timestamp_str TEXT NOT NULL,
        value_raw INTEGER NOT NULL,
        value_str TEXT NOT NULL
    )
    """
    cursor = db_conn.cursor()
    print ("create_table_if_not_exists - Executing: " + sql)
    cursor.execute(sql)
    cursor.close()


def check_if_table_exists_or_else_create(table_name, user_data):
    if not check_if_table_exists_in_cache(table_name):
        if not check_if_table_exists_in_db(table_name, user_data):
            create_table_if_not_exists(table_name, user_data)


def on_message(mqtt_client, user_data, message):
    print ("on_message - received mqtt_client:" + str(mqtt_client) + "user_data: " + str(user_data) + "message: " + str(message))
    payload = message.payload.decode('utf-8')
    table_name = message.topic.split("/")[1]
    print ("on_message - table_name:" + table_name)
    check_if_table_exists_or_else_create(table_name, user_data)
    db_conn = user_data['db_conn']
    sql = 'INSERT INTO ' + table_name + '(timestamp_raw, timestamp_str, value_raw, value_str) VALUES (?, ?, ?, ?)'
    print ("on_message - Executing: " + sql)
    cursor = db_conn.cursor()
    payload_processed = payload.split(",")
    timestamp_raw = payload_processed[0]
    timestamp_str = current_milli_time_to_human(timestamp_raw)
    value_raw = payload_processed[1]
    value_str = payload_processed[2]
    cursor.execute(sql, (timestamp_raw, timestamp_str, value_raw, value_str))
    db_conn.commit()
    cursor.close()
    print ("on_message - Finished processing message!")


def main():
    print ("main - Starting")
    db_conn = sqlite3.connect(DATABASE_FILE)

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    #mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    print ("main - Waiting for Messages...")
    mqtt_client.loop_forever()


main()