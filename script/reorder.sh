#!/bin/bash

img_dir='images'

c=0
for i in `ls $img_dir`
do
  new_name=`printf "frame_%05d.jpg" $c`
  echo $new_name
  cp "$img_dir"'/'"$i" "$img_dir"'/'"$new_name"
  rm "$img_dir"'/'"$i"

  c=`echo $c+1 | bc`
done
