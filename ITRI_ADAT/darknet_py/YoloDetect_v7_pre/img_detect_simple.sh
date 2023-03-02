#!/bin/bash

#img_path='/mnt/sda1/amb_project/ASML_PO/labelclip/001_Connector_normal_1_2d5_/images/frame_00005_01.jpg'
img_path='/home/jklhj/work/ADAT/winbond_facility/20230112_AI_material/Rename_frames/for_test/029_Normal_004'

python3 darknet_detect.py \
       --cfg_file config.txt \
       --resize 0.7 \
       --gpu_idx 0 \
       --thresh 0.25 \
       img_detect \
       --img_path "$img_path" \
       --save_img \
       --save_path 'test.jpg'

       
