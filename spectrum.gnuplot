
set logscale xy
#plot 'build/HER.log' using 2:1
#plot 'build/HER.summary' using 2:1
plot 'build/HER.summary' using 3:2
pause -1
plot 'build/LER.summary' using 3:2
pause -1

#set offset 0,0,1,1
#set style fill solid noborder
#plot 'build/HER.summary' using 1:0:($1*0.5):xtic(1) with boxes
#plot 'build/HER.summary' using 1:0:($1*0.5) with boxes

#pause -1

