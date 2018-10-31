#!/bin/bash

WORKDIR=`echo $PWD`
TRAIN_LMDB='/mnt/sda1/jklhj/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/train_data/train_lmdb'
VAL_LMDB='/mnt/sda1/jklhj/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/val_data/val_lmdb'
SOLVER='resnet_50_solver.prototxt'
GPU_INDEX=1

nvidia-docker run --rm \
  -v "$WORKDIR":/workspace \
  -v "$TRAIN_LMDB":/train_lmdb \
  -v "$VAL_LMDB":/val_lmdb \
  jklhj/caffe-py3 \
  caffe train --solver "$SOLVER" \
  --gpu "$GPU_INDEX" 2>&1 | tee log
