#!/usr/bin/python3
#---------------------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bh1750.py
# Read data from a BH1750 digital light sensor.
#
# Author : Matt Hawkins
# Date   : 26/06/2018
#
# For more information please visit :
# https://www.raspberrypi-spy.co.uk/?s=bh1750
#
#---------------------------------------------------------------------
import smbus
import time
import paho.mqtt.client as mqtt

MQTT_HOST = '192.168.1.36'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'MQTT BH1750 Light Meter'

# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


def current_milli_time():
  return round(time.time() * 1000)


def on_publish(client,userdata,result):             #create function for callback
  print("data published ", result)
  pass


def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data), data

def main():
  mqtt_client = mqtt.Client(MQTT_CLIENT_ID)

  mqtt_client.on_publish = on_publish

  mqtt_client.connect(MQTT_HOST, MQTT_PORT)

  while True:
    lightLevel, data = readLight()
    #print("Light Level : " + format(lightLevel,'.2f') + " lx")
    print(time.strftime('%c %Z') + ',' + format(lightLevel,'.2f'))
    ret = mqtt_client.publish("sensors/bh1750_lux","%s,%s,%s" % (current_milli_time(), data, lightLevel))
    print("Publish Returned: " + str(ret))
    time.sleep(15)

if __name__=="__main__":
   main()
