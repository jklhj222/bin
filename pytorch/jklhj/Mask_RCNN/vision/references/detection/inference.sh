#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

#for i in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.99 1.0
for i in 0.99 
do 

  python3 inference.py \
      --test_dir /home/hugh/tmp/mask_rcnn_PCL_labels/images/images_origin \
      --test_model model_120.pth \
      --num_class 3 \
      --seg_thres "$i" \
      --obj_thres 0.5 \
      --save_fig True 

done                       
