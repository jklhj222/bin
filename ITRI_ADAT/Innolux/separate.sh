#!/bin/bash

for i in 001 002 003 004 005 006 007 008
do
  test -e "$i".data && rm "$i".data
  for j in `ls *.jpg`
  do
    if [ `echo $j | awk -F '_' '{print $NF}'` == $i'.jpg' ]
    then
        echo `realpath $j` >> $i.data
    fi
  done
done
