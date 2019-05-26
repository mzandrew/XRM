#!/bin/bash -e

declare date
declare filename
declare localdir=$(cd $(dirname $(readlink -f $0)); pwd)

cd "$localdir"
mkdir -p pictures
./lights_on.sh
while /bin/true; do
	date=$(date +"%Y-%m-%d.%H%M%S")
	filename="pictures/${date}.jpg"
	./take_pic.sh
	cp -a "pictures/picture.jpg" "$filename"
	echo -n "$date " | tee -a temperatures.log
	./get_temperatures.py | tee -a temperatures.log
	sleep 60
done

