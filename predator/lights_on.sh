#!/bin/bash -e

#16 
echo "1" > /sys/class/gpio/gpio16/value

declare GPIOS="21 20 12 26"
for GPIO in $GPIOS; do
	if [ ! -e "/sys/class/gpio/gpio$GPIO" ]; then
		echo "$GPIO" > /sys/class/gpio/export
	fi
	echo "out" > /sys/class/gpio/gpio$GPIO/direction
	echo "0" > /sys/class/gpio/gpio$GPIO/value
done

