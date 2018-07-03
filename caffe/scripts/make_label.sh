#!/bin/bash

dataset=val

test -e Total_png  && rm -r Total_png || mkdir Total_png
rm "$dataset"_label.dat index_label.dat
rm -r "$dataset"_lmdb Total_png
mkdir Total_png
echo `ls`

j=0
for i in `ls ./ | grep -v make_label | grep -v Total_png | grep -v "$dataset"_label | grep -v convert_lmdb | grep -v index_label | grep -v make_imagenet_mean.sh | grep -v "$dataset"_mean.binaryproto` 
do
  j=`echo "$j+1" | bc` 
  for k in `ls $i`
  do
    echo "$k $j" >> "$dataset"_label.dat
  done

  echo "$j $i" >> index_label.dat
  cp ./$i/*  ./Total_png
 
done 
