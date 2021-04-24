#!/usr/bin/python3 -u

import time
import paho.mqtt.client as mqtt
import requests
import json

MQTT_HOST = '192.168.1.36'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'Accuweather Feed'


def current_milli_time():
    return round(time.time() * 1000)


def on_publish(client,userdata,result):             #create function for callback
    print("data published ", result)
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("Unexpected MQTT disconnection. Will auto-reconnect")


def read_accuweather_feed():
    response = requests.get("")
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return "API ERROR"


mqtt_client = mqtt.Client(MQTT_CLIENT_ID)

mqtt_client.on_publish = on_publish
mqtt_client.on_disconnect = on_disconnect

while True:
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    feed = read_accuweather_feed()
    ret = mqtt_client.publish("sensors/accuweather_upper_holloway", "%s|%s|%s" % (current_milli_time(), str(0), feed))
    print(time.strftime('%c %Z') + ' - Accuweather JSON : ', str(feed))
    time.sleep(1800)
