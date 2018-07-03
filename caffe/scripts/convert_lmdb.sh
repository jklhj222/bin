#!/bin/bash

dataset=train

rm -r "$dataset"_lmdb
GLOG_logtostderr=1 convert_imageset \
       --resize_height=256 \
       --resize_width=256 \
       --shuffle \
       Total_png/ \
       "$dataset"_label.dat \
       "$dataset"_lmdb
