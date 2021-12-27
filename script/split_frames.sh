#!/bin/bash

video_dir='20211224_M7_UCA_25clips'
out_dir="$video_dir"_frames
video_type='.mp4'

mkdir $out_dir

for video in `ls $video_dir`
do
  name=`echo $video | awk -F "$video_type" '{print $1}'`
  echo $i $name

  mkdir "$out_dir"'/'"$name"
  ffmpeg -i "$video_dir"'/'"$video" "$out_dir"'/'"$name"'/frame_%05d.jpg'

done
