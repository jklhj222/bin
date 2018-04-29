#!/bin/bash

j=0
rm train_label.dat label_index_string.dat
mkdir Total_png
for i in Black-grass Charlock Cleavers Common_Chickweed Common_wheat Fat_Hen Loose_Silky-bent Maize Scentless_Mayweed Shepherds_Purse Small-flowered_Cranesbill Sugar_beet
do
  j=`echo "$j+1" | bc`
  cp $i/* ./Total_png/
  ls -l ./$i | grep png | awk '{print $9" "j}' j=$j >> train_label.dat
  echo $j $i >> train_index_string.dat
  echo $j $i done
done 
