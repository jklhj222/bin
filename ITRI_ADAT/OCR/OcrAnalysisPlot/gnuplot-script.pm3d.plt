unset key

set xlabel "X"
set ylabel "Y"
set zlabel "Score"

set pm3d
set xyplane 3
set hidden3d
set pm3d map
set pm3d interpolate 0,0
set size square
#set size ratio 4.07 
set cbrange [0:1]

set xrange [0:14]
set yrange [-14:0]

splot   'all_scores.txt'   with   lines

set output "contour.png"
set terminal png

pause -1
