set xdata time
set timefmt "%Y-%m-%d.%H%M%S"
#set format x "%Y\n%m/%d\n%H:%M"
#set format x "%H:%M"
#set format x "%Hh"
set format x "%m-%d\n%Hh"
#set key right center
#set key right
set key left bottom box opaque
#set xrange ['2019-05-28.143000' : '2019-05-29.143000']
#set xrange ['2019-06-03.085600' : '2019-06-04.085600']
#set xrange ['2019-06-03.000000' : '2019-06-03.235959']
set xrange [ xrange_start : xrange_end ] 
set mxtics 6

set yrange [20:30]
set mytics 2
#set yrange [-5:40]
set ylabel "temperature (C)"

#set autoscale y2
set y2range [0.0:0.5]
set y2tics
set my2tics 2
set y2label "amplifier current (A)"
current_fudge=4.0

set terminal png size 1022,260
set output "pictures/temperatures.png"
set lmargin 9
set rmargin 12
#set style line 1 linewidth 40

#plot "logs/temperatures.log" using 1:2 title "ambient", "temperatures.log" using 1:(22+$2-$3) with linespoints title "copper"
#plot "logs/temperatures.log" using 1:2 with lines linewidth 2 title "ambient", "temperatures.log" using 1:(47-$3) with lines linewidth 2 title "copper"
#plot "logs/temperatures.log" using 1:2 with lines linewidth 2 title "ambient"
plot \
	"logs/temperatures.log" using 1:3 axes x1y1 with lines linewidth 2 title "Cu temp", \
	"logs/temperatures.log" using 1:2 axes x1y1 with lines linewidth 2 title "ref temp", \
	"logs/temperatures.log" using 1:4 axes x1y1 with lines linewidth 2 title "ADC temp", \
	"logs/temperatures.log" using 1:(($6-$5)/0.01/current_fudge) axes x1y2 with lines linewidth 2 title "amplifier I"

#pause -1

