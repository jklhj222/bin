#!/bin/bash

for i in `ls *.zip | awk -F '.zip' '{print $1}'`
do
  mkdir $i
  cd $i
  unzip ../"$i".zip
  cd ..
done
