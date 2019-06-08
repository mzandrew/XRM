#!/bin/bash

declare string="$(ps ax)"
declare instances_already_running=$(echo "$string" | grep -v "sudo" | grep -c "daemon.sh")
if [ $instances_already_running -gt 1 ]; then
	echo "daemon.sh already running"
	echo "$string" | grep "daemon.sh"
	exit 0
fi

sleep 10

declare date
declare picfile
declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)
declare logfile="logs/temperatures.log"

cd "$localdir"
mkdir -p pictures
./lights_on.sh
while /bin/true; do
	date=$(date +"%Y-%m-%d.%H%M%S")
	#echo -n "$date " | tee -a "$logfile"
	./get_temperatures.py $date >> "$logfile"
	picfile="pictures/${date}.jpg"
	./take_pic.sh
	cp -a "pictures/picture.jpg" "$picfile"
	sleep 60
done

