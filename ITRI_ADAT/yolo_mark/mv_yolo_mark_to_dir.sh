#!/bin/bash

mkdir images labels

for i in `ls *.txt | grep -v train.txt`
do
  filename=`echo $i | awk -F '.txt' '{print $1}'`
  echo $filename

  mv "$filename"'.txt' labels
  mv "$filename"'.jpg' images

done

