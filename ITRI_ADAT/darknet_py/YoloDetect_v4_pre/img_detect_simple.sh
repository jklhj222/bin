#!/bin/bash

img_path='/mnt/sda1/amb_project/ASML_PO/labelclip/001_Connector_normal_1_2d5_/images/frame_00005_01.jpg'

python3 darknet_detect.py \
       --cfg_file config.txt \
       --resize 0.7 \
       --gpu_idx 0 \
       --thresh 0.25 \
       img_detect \
       --img_path "$img_path" \
       --save_img \
       --save_path '001_Connector_normal_1_2d5_/'"frame_00005_01.jpg"

       
