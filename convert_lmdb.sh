#!/bin/bash

train_val='train'

rm -r "$train_val"_lmdb
GLOG_logtostderr=1 convert_imageset \
        --resize_height=300 \
        --resize_width=300 \
        --shuffle \
        Total_png/ \
        "$train_val"_label.dat \
        "$train_val"_lmdb
