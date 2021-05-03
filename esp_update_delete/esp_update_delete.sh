#!/bin/sh

set -x
echo "Running:"
tail -f -n 0 /usr/local/nginx/logs/access.log | awk '
                    /OutdoorWeatherStation/ { system("echo Sleep 10s;sleep 10;rm -rf /home/birdofprey/esp8266/OutdoorWeatherStation.ino.esp8285.bin;echo Result: $?") }'

