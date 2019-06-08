#!/bin/bash -e

declare GPIOS="21 20 16 12 26"
for GPIO in $GPIOS; do
	if [ ! -e "/sys/class/gpio/gpio$GPIO" ]; then
		echo "$GPIO" > /sys/class/gpio/export
	fi
	echo "out" > /sys/class/gpio/gpio$GPIO/direction
	echo "1" > /sys/class/gpio/gpio$GPIO/value
done

