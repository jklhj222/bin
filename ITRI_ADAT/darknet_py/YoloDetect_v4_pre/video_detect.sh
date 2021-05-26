#!/bin/bash

video_path='/mnt/sdb1/work/ADAT/AIDC/AI_Samples_20210511/TestData/02_Test2.mp4'

python3 darknet_detect.py \
       --cfg_file config.txt \
       --resize 0.7 \
       --gpu_idx 0 \
       --thresh 0.1 \
       video_detect \
       --video_path "$video_path" \
       --check_delay 50
# --save_video

       
