#!/bin/bash -e

declare output_size="3840x2160"
#output_size="1920x1080"
output_size="1024x576"
#output_size="800x450"
declare output_filename="XRM-HER-next-try.mp4"
declare -i xi=275 w=425
declare -i yi=77 h=170
declare -i last_frame_number=701
declare -i fps=1

#time ffmpeg -r 60 -f image2 -pattern_type glob -i "*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p -s $output_size $output_filename
#time ffmpeg -r 60 \
#	-f image2 -pattern_type glob -i "*.jpg" \
#	-i ~/build/2019-05-29.1430.superkekb.dailysnap.gif -filter_complex "[0:v][1:v] overlay=0:0" \
#	-vcodec libx264 -crf 25  -pix_fmt yuv420p -s $output_size $output_filename

declare -i line_height=$((750+260))
declare slope=$(echo "$w/$last_frame_number" | bc -l)
declare -i step=$(echo "(1/$slope)/1" | bc)
if [ $step -eq 0 ]; then
	step=1
fi
#echo "slope=$slope step=$step"
drawline_string=""
for n in $(seq 0 $step $((last_frame_number-1))); do
	if [ $n -gt 0 ]; then
		drawline_string="$drawline_string, "
	fi
	drawline_string="$drawline_string drawbox=enable='between(n,$n,$((n+step)))':x=$(echo "($xi+$slope*$n+0.5)/1" | bc):y=0:w=3:h=$line_height:c=blue"
done
#echo "$drawline_string"
#exit 0
	#-i ~/build/XRM/predator/pictures/2019-05-29.1430.superkekb.dailysnap.gif \
	#-i ~/build/XRM/predator/pictures/temperatures.png \
	#-filter_complex "[0:v][1:v] overlay=0:0[a], [a][2:v] overlay=0:750, $drawline_string, drawbox=x=$xi:y=$yi:w=$w:h=$h:c=green:t=2" \

time ffmpeg \
	-r $fps \
	-f image2 \
	-pattern_type glob -i "/media/mza/rootfs/home/pi/build/XRM/predator/pictures/2019-06*.jpg" \
	-vcodec libx264 \
	-crf 25 \
	-pix_fmt yuv420p \
	-s $output_size \
	$output_filename
echo; echo "mplayer -loop 0 $output_filename"
	#-filter_complex "[0:v][1:v] overlay=0:0, drawbox=$xi:$yi:$w:$h:green, drawbox=$xi+$slope*t/$fps:0:3:750:blue" \
	#, [c]trim=0:1[hold];[c][hold]concat[extended];[extended][c]overlay
	#[c], [c]trim=0:1[hold];[c][hold]concat[extended];[extended][c]overlay
#ffmpeg -ss 00:00:11.50 -i $output_filename -frames:v 1 $output_filename.jpg

