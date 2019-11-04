#!/bin/bash

for i in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
do 

  python3 inference2.py \
      --test_dir /home/hugh/tmp/mask_rcnn_PCL_labels/images/image_resize_allRec/test \
      --test_model model_2000.pth \
      --num_class 3 \
      --seg_thres "$i" \
      --save_fig True 

done                       
