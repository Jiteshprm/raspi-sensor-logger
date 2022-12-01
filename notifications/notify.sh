#!/bin/sh
if ! [ -z "$2" ]; then # execute the next line if there is a second parameter on the script's command line
	sleep $2 # pause for the length of time indicated by the second parameter
fi

TIMESTAMP_NOW=$(date +"%m-%d-%Y_%Hh%Mm%Ss")
FILE_CRASH_PATH="/tmp/crash_${1}_${TIMESTAMP_NOW}.txt"
journalctl -u "${1}" > "${FILE_CRASH_PATH}"

# I have sendmail installed on my Pi - use the appropriate syntax if you use a different mail handler
# The <<EOF....EOF sequence directs everything from the line below that on which the <<EOF appears to the
# second EOF to sendmail, creating an email message. I have the root address aliased to my regular email.
#cat <<EOF | msmtp birdofp@gmail.com
#To: birdofp
#From: raspberry
#Subject: Raspberry - $1 service restarted!
#
## Crash File name
#${FILE_CRASH_PATH}
#
## Include the reporting service's status
#$(systemctl status -l -n 50 "$1")
#EOF