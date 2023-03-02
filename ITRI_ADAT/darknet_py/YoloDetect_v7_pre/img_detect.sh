#!/bin/bash

img_dir='/mnt/sda1/work/ASML/20211222_ASML_YS_29clips_frames/016_Connector_abnormal_8/768x432'
output_dir='016_Connector_abnormal_8_2d5_'

mkdir $output_dir

for img_path in `ls "$img_dir"/*.jpg`
do
  echo $img_path
  base=`basename $img_path`
  echo  $base
  output_path="$output_dir"'/'"$base"  
  echo $output_path

  python3 darknet_detect.py \
         --cfg_file config.txt \
         --resize 0.7 \
         --gpu_idx 0 \
         --thresh 0.25 \
         img_detect \
         --img_path "$img_path" \
         --save_img \
         --save_path "$output_path" \
         --noshow_img 

done

       
