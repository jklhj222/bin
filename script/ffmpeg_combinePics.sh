#!/bin/bash

for i in 002_USI_002_helmet 003_USI_003_head 004_USI_004_head 005_USI_005_head 007_USI_007_helmet 
do
  start_number=`ls $i | head -1 | awk -F '.jpg' '{print $1}' | awk -F '_' '{print $2}'`
  ffmpeg -r 60 -start_number "$start_number" -i "$i"/frame_"%5d.jpg" -r 30 -vf "scale=1920:-2" "$i".mp4
done
