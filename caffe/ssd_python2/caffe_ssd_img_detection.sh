#!/bin/bash

python2 caffe_ssd_img_detection.py \
         --root_caffe_ssd /home/hugh/pkg/local/caffe_ssd_python2 \
         --set_gpu \
         --gpu_index 1 \
         --deploy_model deploy.prototxt \
         --pretrain_model VGG_KITTI_SSD_500x500_iter_120000.caffemodel \
         --image_file /mnt/sda1/work/Aviation/Aviation_20180820/AACL_AI_Training_material_20180820_training/Down/data_00135/images/frame00659.jpg \
         --show_img
