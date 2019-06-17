#!/bin/bash

for i in `ls *_orig.jpg`
do

  filename=`echo "$i" | awk -F '_orig.jpg' '{print $1}'`
  filename1="$i"
  filename2=`echo "$i" | awk -F '_orig.jpg' '{print $1".jpg"}'`

  python3 img_combine.py --imgs "['"$filename1"', '"$filename2"']" --out_img "$filename"'_combine.jpg'

done
