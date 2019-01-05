#!/bin/bash

#for i in `ls -d data_*`
#do
  for j in `ls ./images/`
  do
    echo ./images/"$j"
    python3 brightness.py <<< ./images/"$j"

  done
#done
