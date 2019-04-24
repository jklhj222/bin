#!/bin/bash

for dis in 10 11 12 13 14 15 20 27
do
  cd dis"$dis"

  for file in `ls`
  do
    file_id=`echo $file | awk -F '.jpg' '{print $1}'`
    tesseract "$file" "$file_id"'_output' -l eng

    echo 'dis'"$dis" "$file" 
  done

  cd ..
done
      

