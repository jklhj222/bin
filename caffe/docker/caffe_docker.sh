#!/bin/bash

WORKDIR=`echo $PWD`
TRAIN_LMDB='/mnt/sda1/jklhj/Plant_Seedlings_Classification/jklhj/Caffe_ResNet50/test2/tmp/train_lmdb'
VAL_LMDB='/mnt/sda1/jklhj/Plant_Seedlings_Classification/jklhj/Caffe_ResNet50/test2/tmp/val_lmdb'
SOLVER='resnet_50_solver.prototxt'
GPU_INDEX=1

nvidia-docker run --rm \
  -v "$WORKDIR":/workspace \
  -v "$TRAIN_LMDB":/workspace/train_lmdb \
  -v "$VAL_LMDB":/workspace/val_lmdb \
  jklhj/caffe-py3 \
  caffe train --solver "$SOLVER" \
  --gpu "$GPU_INDEX" 2>&1 | tee log
