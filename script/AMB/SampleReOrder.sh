#!/bin/bash

read -p 'Initial index: ' init
read -p 'Video numbers: ' num
read -p 'Type name: ' type_name
#init=24
#num=9
#type_name='AbnormalHigh'

mkdir 'Rename'
mkdir 'Orig'

idx=$init
sub_idx=1
for i in `ls *.mp4 | head -$num`
do
  newname=`printf "%03d_%s_%03d.mp4" $idx $type_name $sub_idx`
  echo $newname
  cp $i  'Rename/'"$newname"
  mv $i 'Orig/'

  idx=`echo $idx + 1 | bc`
  sub_idx=`echo $sub_idx + 1 | bc`
done
