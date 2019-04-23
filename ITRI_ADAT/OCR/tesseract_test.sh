#!/bin/bash

for dis in 10 11 12 13 14 15 20 27
do
  cd dis"$dis"
  
  for x in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
  do
    for y in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
    do
      tesseract 'dis'"$dis"'_font3_'"$y"'_'"$x"'.jpg' 'dis'"$dis"'_font3_'"$y"'_'"$x"'_output' -l eng

      echo 'dis'"$dis"'_font3_'"$y"'_'"$x"
    done
  done

  cd ..
done
