#!/bin/bash

for i in a b c d
do
  temp=`sudo /usr/sbin/smartctl --all /dev/sd"$i" | grep Temp | awk '{print $10}'`
  echo sd"$i"_temp = "$temp"C
done
