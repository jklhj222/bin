#!/bin/bash

#read -p 'the number of rows: ' rows
#read -p 'the number of columns: ' cols

rows=`echo "$1"-1 | bc`
cols=`echo "$2"-1 | bc`

echo 'rows: 0 to '"$rows"
echo 'cols: 0 to '"$cols"

#for dis in 10 11 12 13 14 15 20 27
#do
#  cd dis"$dis"
  cd 'split'
 
  for col in `seq 0 $cols`
  do
    for row in `seq 0 $rows` 
    do
#      tesseract 'dis'"$dis"'_font3_'"$y"'_'"$x"'.jpg' 'dis'"$dis"'_font3_'"$y"'_'"$x"'_output' -l eng
      tesseract "$col"'_'"$row"'.jpg' "$col"'_'"$row"'_output' -l eng

#      echo 'dis'"$dis"'_font3_'"$y"'_'"$x"
      echo "$col"'_'"$row"'.jpg'
    done
  done

  cd ..
#done
