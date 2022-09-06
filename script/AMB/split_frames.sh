#!/bin/bash

read -p 'video_dir: ' video_dir
#video_dir='20211224_M7_UCA_25clips'
video_type='.mp4'
out_dir="$video_dir"_frames

mkdir $out_dir

for video in `ls $video_dir`
do
  name=`echo $video | awk -F "$video_type" '{print $1}'`
  echo $i $name

  mkdir "$out_dir"'/'"$name"
  # -qscale normal range for JPEG is 2-31 with 31 being the worst quality.
  # You can use a value of 1 but you must add the -qmin 1 output option (because the default is -qmin 2).
  ffmpeg -i "$video_dir"'/'"$video" -qmin 1 -qscale:v 2 "$out_dir"'/'"$name"'/frame_%05d.jpg'

done
