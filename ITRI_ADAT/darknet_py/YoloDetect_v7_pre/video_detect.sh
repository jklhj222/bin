#!/bin/bash

video_dir='/mnt/sdc1/Dropbox/tmp-PC/AIDC/AI_Samples_20210511/TestData/'

read -p 'Execute? (y/n)   ' yn
if [ "$yn" == 'y' ] || [ "$yn" == 'Y' ]
then
    echo 'Excute now'
elif [ "$yn" == 'n' ] || [ "$yn" == 'N' ]
then
    echo 'Dont execute'
    exit
else
    echo 'Dont execute'
    exit
fi

for i in `ls $video_dir`
do
    filename=`echo $i | awk -F '.mp4' '{print $1}'`
    video_path="$video_dir"'/'"$i"
    echo 'video_path '"$video_path"

    if [ -d "out_images" ]
    then
        rm -r out_images
    fi
    if [ -f "$filename"'_inference.mp4' ]
    then
        rm -r "$filename"'_inference.mp4'
    fi
    if [ -d "$filename"'_inferenceImgs' ]
    then
        rm -r "$filename"'_inferenceImgs'
    fi
    
    python3 darknet_detect.py \
           --cfg_file config.txt \
           --resize 0.7 \
           --gpu_idx 0 \
           --thresh 0.25 \
           video_detect \
           --video_path "$video_path" \
           --check_delay 10   --save_video --save_images \
           2>&1 | tee log

    mv log "$filename"'_inference_log'
    mv output.avi "$filename"'_inference.mp4'
    mv out_images "$filename"'_inferenceImgs'

done
       
