#!/bin/bash

export CUDA_VISIBLE_DEVICES=1

python3 train.py --num-class 3 \
                 --save-epoch 30 \
                 --eval-epoch 30 \
                 --lr 0.001 \
                 --lr-steps 30 60 90 \
                 --epochs 120 \
                 --data-path /home/hugh/tmp/sophie_20191031/jklhj/images_2class/image_resize \
                 | tee log 
