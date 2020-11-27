#!/bin/bash

img_path='tmp.jpg'

python3 darknet_detect.py \
       --cfg_file config.txt \
       --resize 0.7 \
       --gpu_idx 0 \
       --thresh 0.25 \
       img_detect \
       --img_path "$img_path" # --save_img


       
