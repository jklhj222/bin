#!/bin/bash


for file in `ls *.mp4`
do
  echo $file >> tmp.dat
done 

count=1
for i in 0 5 6 7 8 9
do
  for j in 45 60
  do
    for k in 15 20 25
    do
 
      file=`cat tmp.dat | head -"$count" | tail -1`

      cp "$file" Side_screw_"$i"turn_"$k"D_"$j"H.mp4

      count=`echo $count+1 | bc`
      echo $count
      echo $file
      echo Side_screw_"$i"turn_"$k"D_"$j"H.mp4
      echo 

    done
  done
done

rm tmp.dat
