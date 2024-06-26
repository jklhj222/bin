#!/bin/bash

for i in `ls *.jpg`
do

  file=`echo $i | awk -F '.jpg' '{print $1}'`
  
  convert -rotate 90 "$file".jpg "$file"_rotate90.jpg
  python3 yolo_rotate90.py <<< "$file".jpg
  mv tmp.dat "$file"_rotate90.txt

  convert -rotate 90 "$file"_rotate90.jpg "$file"_rotate180.jpg
  python3 yolo_rotate90.py <<< "$file"_rotate90.jpg
  mv tmp.dat "$file"_rotate180.txt

  convert -rotate 90 "$file"_rotate180.jpg "$file"_rotate270.jpg
  python3 yolo_rotate90.py <<< "$file"_rotate180.jpg
  mv tmp.dat "$file"_rotate270.txt

done

for i in `ls *.png`
do

  file=`echo $i | awk -F '.png' '{print $1}'`
  
  convert -rotate 90 "$file".png "$file"_rotate90.png
  python3 yolo_rotate90.py <<< "$file".png
  mv tmp.dat "$file"_rotate90.txt

  convert -rotate 90 "$file"_rotate90.png "$file"_rotate180.png
  python3 yolo_rotate90.py <<< "$file"_rotate90.png
  mv tmp.dat "$file"_rotate180.txt

  convert -rotate 90 "$file"_rotate180.png "$file"_rotate270.png
  python3 yolo_rotate90.py <<< "$file"_rotate180.png
  mv tmp.dat "$file"_rotate270.txt

done
