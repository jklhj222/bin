#!/bin/bash

rm tmp.dat

for i in `ls *.txt`
do
  while IFS= read -r line
  do
    echo -ne "$line" >> tmp.dat
    
  done < $i 

  echo -ne '\n' >> tmp.dat

  cp tmp.dat $i
  rm tmp.dat

done
