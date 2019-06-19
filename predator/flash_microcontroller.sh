#!/bin/bash -e

function flash_bootloader {
	cd ${HOME}/build
	local dir="v3.6.0"
	local filename="update-bootloader-circuitplay_m0-v3.6.0.uf2"
	if [ ! -e $filename ]; then
		wget -q https://github.com/adafruit/uf2-samdx1/releases/download/$dir/$filename
	fi
	sudo mount /dev/sda /media && sudo cp $filename /media/ && sudo umount /media
	sleep 1
	sudo fdisk -l /dev/sda
}

function unbrick {
	cd ${HOME}/build
	while /bin/true; do sudo mount /dev/sda /media && sudo cp update-bootloader-circuitplay_m0-v3.6.0.uf2 /media/ && sudo umount /media && break; done
}

function flash_circuitpython {
	cd ${HOME}/build
	local dir="4.0.1"
	local filename="adafruit-circuitpython-circuitplayground_express-en_US-4.0.1.uf2"
	if [ ! -e $filename ]; then
		wget -q https://github.com/adafruit/circuitpython/releases/download/$dir/$filename
	fi
	sudo mount /dev/sda /media && sudo cp $filename /media/ && sudo umount /media
	sleep 5
	sudo fdisk -l /dev/sda
}

function erase_circuitpython_drive {
	sudo mount /dev/sda1 /media
	sudo rsync -t ./microcontroller/erase.py /media/boot.py
	sleep 1
	sudo fdisk -l /dev/sda
}

# /etc/fstab
#/dev/sda1 /media vfat defaults,noatime,users 0 0

#flash_bootloader
#unbrick
flash_circuitpython
#erase_circuitpython_drive

