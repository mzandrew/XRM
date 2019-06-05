#!/bin/bash -e

function go {
	local date="${1}"
	local date1=$(date +"%Y%m%d" -d "$date +1 day") date2=$(date +"%Y-%m-%d" -d "$date") YYYY=$(date +"%Y" -d $date) MM=$(date +"%m" -d $date)
	local filename1="dailysnap-${date1}-0000.png"
	local filename2="${date2}.superkekb.png"
	echo "$filename1 $filename2"
	local url="http://www-linac.kek.jp/skekb/snapshot/ring"
	#url="$url/dailysnap-$YYYY/dailysnap-$YYYY-$MM"
	if [ ! -e "pictures/$filename2" ]; then
		echo "grabbing daily snapshot..."
		wget -q $url/$filename1 -O pictures/$filename2
	fi
	echo "plotting temperatures..."
	gnuplot -e "xrange_start='${date2}.000000'" -e "xrange_end='${date2}.235959'" temperatures.gnuplot
	if [ -s "pictures/$filename2" ] && [ -s "pictures/temperatures.png" ]; then
		convert pictures/$filename2 pictures/temperatures.png -append pictures/${date2}.superkekb-with-temperatures.png
	else
		echo -n "Missing or zero-length:" > /dev/stderr
		if [ ! -s "pictures/$filename2" ]; then
			echo -n " pictures/$filename2" > /dev/stderr
		fi
		if [ ! -s "pictures/temperatures.png" ]; then
			echo -n " pictures/temperatures.png" > /dev/stderr
		fi
		echo > /dev/stderr
		exit 1
	fi
	ls -lart pictures/$filename2 pictures/temperatures.png pictures/${date2}.superkekb-with-temperatures.png
	#sleep 1
}

#echo $HOSTNAME
#if [ "$HOSTNAME" != "raspberrypi" ]; then
#	rsync xrmrpi:build/XRM/predator/temperatures.log .
#fi

#for day in $(seq 28 30); do
#	go 2019-05-$day
#done
# historical images are archived in dailysnap-2019/dailysnap-2019-05/

#go yesterday
go today # doesn't make sense, since the day's final snapshot is not yet generated, but still useful when across the international date line from KEK

