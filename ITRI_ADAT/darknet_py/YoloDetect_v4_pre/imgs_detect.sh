#!/bin/bash


for imgs_dir in `ls /mnt/sda1/work/ASML/20220127_M7_UCA_14clips_frames/for_test`
do
  echo imgs_dir = "$imgs_dir"

  imgs_path='/mnt/sda1/work/ASML/20220127_M7_UCA_14clips_frames/'"$imgs_dir"'/768x432'
  output_dir="$imgs_dir"'_2d5_'

  mkdir $output_dir

  echo $imgs_path

  python3 darknet_detect.py \
          --cfg_file config.txt \
          --resize 0.7 \
          --gpu_idx 0 \
          --thresh 0.7 \
          imgs_detect \
          --imgs_path "$imgs_path" \
          --output_dir "$output_dir" \
          --save_img \
          --noshow_img 

done

