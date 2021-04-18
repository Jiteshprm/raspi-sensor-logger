#!/bin/sh
if ! [ -z "$2" ]; then # execute the next line if there is a second parameter on the script's command line
	sleep $2 # pause for the length of time indicated by the second parameter
fi

# I have sendmail installed on my Pi - use the appropriate syntax if you use a different mail handler
# The <<EOF....EOF sequence directs everything from the line below that on which the <<EOF appears to the
# second EOF to sendmail, creating an email message. I have the root address aliased to my regular email.
echo "Subject: Notification Email for $1 service \n # Include the reporting service's status\n $(systemctl status -l -n 50 "$1")" | msmtp birdofp@gmail.com
