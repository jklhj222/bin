#!/bin/bash

img_file='test.jpg'
filename=`echo $img_file | awk -F '.' '{print $1}'`
fileext=`echo $img_file | awk -F '.' '{print $2}'`

convert -monochorme "$img_file" "$filename"'_mono.'"$fileext"
convert -threshold 50% "$img_file" "$filename"'_thres.'"$fileext"
