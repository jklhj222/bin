#!/bin/bash

for i in `ls -d ./data_*`
do
  for j in `ls "$i"/labels/`
  do
    echo "" >> "$i"/labels/"$j"
  done
done
