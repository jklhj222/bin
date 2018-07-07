#!/bin/bash

sudo nvidia-docker run  -v /mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/jklhj/Caffe_AlexNet_SGD_mean_new/tmp:/workspace -v /mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10_224/train_data/:/data/train -v /mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10_224/val_data/:/data/val bvlc/caffe-jklhj:gpu bash -c "caffe train --solver=./solver.prototxt 2> log"
