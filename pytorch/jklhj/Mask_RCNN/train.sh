#!/bin/bash

#export CUDA_VISIBLE_DEVICES=0,1

python3 -m torch.distributed.launch \
                 --nproc_per_node=2 --use_env train.py \
                 --num-class 14 \
                 --save-epoch 1000 \
                 --eval-epoch 1000 \
                 --lr 0.001 \
                 --lr-steps 1000 2000 3000 \
                 --epochs 3500 \
                 --aspect-ratio-group-factor 3 \
                 --data-path /home/hugh/tmp/A14_labels_cut/Image \
                 | tee log 
