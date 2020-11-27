#!/bin/bash

video_path='/home/hugh/Downloads/MIRDC_2/MIRDC_sampling_20201120/20201120_110641_HoloLens.mp4'

python3 darknet_detect.py \
       --cfg_file config.txt \
       --resize 0.7 \
       --gpu_idx 0 \
       --thresh 0.25 \
       video_detect \
       --video_path "$video_path" # --save_video


       
