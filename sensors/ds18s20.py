#!/usr/bin/python3
import os
import glob
import time
import paho.mqtt.client as mqtt

MQTT_HOST = '192.168.1.36'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'MQTT DS18S20 Temperature Meter'

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def current_milli_time():
    return round(time.time() * 1000)


def on_publish(client,userdata,result):             #create function for callback
    print("data published ", result)
    pass


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return str(temp_c), lines


mqtt_client = mqtt.Client(MQTT_CLIENT_ID)

mqtt_client.on_publish = on_publish

mqtt_client.connect(MQTT_HOST, MQTT_PORT)

while True:
    temp_c, lines = read_temp()
    print(time.strftime('%c %Z') + ',' + str(temp_c))
    ret = mqtt_client.publish("sensors/ds18s20_temp","%s,%s,%s" % (current_milli_time(), lines, temp_c))
    print("Publish ds18s20_temp Returned: " + str(ret))
    time.sleep(15)
