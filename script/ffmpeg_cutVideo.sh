#!/bin/bash

#ffmpeg  -ss  00:00:10.000  -to 00:00:28.000  -i  /home/hugh/pkg/local/DeepFaceLab/Alpha_test_demo.mp4  -map  0:v:0  -map  0:a:0?  -b:v  3M  -c:v  libx264  -pix_fmt  yuv420p  /home/hugh/pkg/local/DeepFaceLab/Alpha_test_demo_cut.mp4  -y

ffmpeg  -i  /home/hugh/pkg/local/DeepFaceLab/Alpha_test_demo.mp4  -ss  00:00:10.000  -to 00:00:28.000  -map  0:v:0  -map  0:a:0?  -b:v  25M  -c:v  libx264  -pix_fmt  yuv420p  -strict -2  /home/hugh/pkg/local/DeepFaceLab/Alpha_test_demo_cut.mp4  -y

#ffmpeg -i  /home/hugh/pkg/local/DeepFaceLab/Alpha_test_demo.mp4 -ss  00:00:10.000  -to 00:00:28.000  -strict -2  /home/hugh/pkg/local/DeepFaceLab/Alpha_test_demo_cut.mp4  
