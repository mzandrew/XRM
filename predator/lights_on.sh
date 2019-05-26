#!/bin/bash -e

if [ ! -e /sys/class/gpio/gpio17 ]; then
	echo "17" > /sys/class/gpio/export
fi
if [ ! -e /sys/class/gpio/gpio22 ]; then
	echo "22" > /sys/class/gpio/export
fi
echo "out" > /sys/class/gpio/gpio17/direction
echo "out" > /sys/class/gpio/gpio22/direction
echo "0" > /sys/class/gpio/gpio17/value
echo "0" > /sys/class/gpio/gpio22/value

