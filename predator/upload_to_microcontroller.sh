#!/bin/bash -e

#declare device="/dev/sda"
#declare device="/dev/sdb" # for when you don't umount cleanly...
declare list="" microcontroller_list="" media_list=""
declare potential_list="code.py samd21_get_temperature.py light_follows_button.py erase.py"

function find_and_show {
	list="" microcontroller_list="" media_list=""
	for file in $potential_list; do
		dir="./microcontroller"
		if [ -e "$dir/$file" ]; then
			microcontroller_list="$list $dir/$file"
			list="$list $dir/$file"
		fi
		dir="/media"
		if [ -e "$dir/$file" ]; then
			media_list="$list $dir/$file"
			list="$list $dir/$file"
		fi
	done
	ls -lart $list
}

if [ ! -e /media/boot_out.txt ]; then
	mount /media
	if [ ! -e /media/boot_out.txt ]; then
		echo "error mounting /media"
		exit 1
	fi
fi
find_and_show
rsync -t $microcontroller_list /media/
sync
echo "----"
find_and_show
umount /media

