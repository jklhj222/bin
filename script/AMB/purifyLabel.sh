#!/bin/bash

for i in `ls *.txt`
do
  fname=`echo $i | awk -F '.txt' '{print $1}'`


  if [ -f "$fname"'.jpg' ]
  then
      echo $i "$fname"'.jpg'
  else
      echo 'remove ' $i
      rm $i
  fi


done
