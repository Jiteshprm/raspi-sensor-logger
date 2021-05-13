#!/bin/sh

set -x
echo "Running:"
while true
do
  mosquitto_sub -h 127.0.0.1 -v -C 1 -t sensors/outdoor_update
  echo Sleep 30s
  sleep 30
  rm -rf /home/birdofprey/esp8266/OutdoorWeatherStation.ino.generic.bin
  echo Result: $?
done
