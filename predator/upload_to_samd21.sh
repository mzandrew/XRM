#!/bin/bash -e

declare device="/dev/sda"
#declare device="/dev/sdb" # for when you don't umount cleanly...

#if [ -e /media/code.py ]; then
#	sudo umount /media
#fi
sudo mount ${device}1 /media
sudo rsync -t samd21_get_temperature.py /media/code.py
sudo umount /media

