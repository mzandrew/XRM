#!/bin/bash -e

declare -i n=5 i=1

if [ $# -gt 0 ]; then
	n=$1
fi
#echo $n

#declare GPIOS="21 16 20 12 26"
declare GPIOS="20 21 26 16 12"
for GPIO in $GPIOS; do
	if [ ! -e "/sys/class/gpio/gpio$GPIO" ]; then
		echo "$GPIO" > /sys/class/gpio/export
	fi
	if [ ! "$(cat /sys/class/gpio/gpio$GPIO/direction)" = "out" ]; then
		echo "out" > /sys/class/gpio/gpio$GPIO/direction
	fi
	if [ $i -le $n ]; then
		echo "1" > /sys/class/gpio/gpio$GPIO/value
	else
		echo "0" > /sys/class/gpio/gpio$GPIO/value
	fi
	i=$((i+1))
done

