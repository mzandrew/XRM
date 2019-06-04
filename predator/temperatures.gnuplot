set xdata time
set timefmt "%Y-%m-%d.%H%M%S"
#set format x "%Y\n%m/%d\n%H:%M"
#set format x "%H:%M"
set format x "%Hh"
set key right center
#set xrange ['2019-05-28.143000' : '2019-05-29.143000']
set xrange ['2019-06-03.085600' : '2019-06-04.085600']

set terminal png size 1022,260
set output "pictures/temperature.png"
set lmargin 9
set rmargin 12
#set style line 1 linewidth 40

#plot "temperatures.log" using 1:2 title "ambient", "temperatures.log" using 1:(22+$2-$3) with linespoints title "copper"
#plot "temperatures.log" using 1:2 with lines linewidth 2 title "ambient", "temperatures.log" using 1:(47-$3) with lines linewidth 2 title "copper"
plot "temperatures.log" using 1:2 with lines linewidth 2 title "ambient"
#plot "temperatures.log" using 1:2 with lines linewidth 2 title "ambient", "temperatures.log" using 1:3 with lines linewidth 2 title "copper"

#pause -1

