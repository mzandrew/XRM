#!/bin/bash -e

function go {
	local date="${1}"
	local date1=$(date +"%Y%m%d" -d "$date +1 day") date2=$(date +"%Y-%m-%d" -d "$date")
	local filename1="dailysnap-${date1}-0000.png"
	local filename2="${date2}.superkekb.png"
	echo "$filename1 $filename2"
	if [ ! -e "pictures/$filename2" ]; then
		wget -q http://www-linac.kek.jp/skekb/snapshot/ring/$filename1 -O pictures/$filename2
	fi
	gnuplot -e "xrange_start='${date2}.000000'" -e "xrange_end='${date2}.235959'" temperatures.gnuplot
	if [ ! -s "pictures/$filename2" ] && [ ! -s pictures/temperatures.png ]; then
		convert pictures/$filename2 pictures/temperatures.png -append pictures/${date2}.superkekb-with-temperatures.png
	fi
	ls -lart pictures/$filename2 pictures/temperatures.png pictures/${date2}.superkekb-with-temperatures.png
	sleep 1
}

#go today
go 2019-06-04

#for day in $(seq 28 30); do
#	go 2019-05-$day
#done
# historical images are archived in dailysnap-2019/dailysnap-2019-05/

