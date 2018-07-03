#!/bin/bash
# 2018/07/02
# Usage: need label file 
#        produce lmdb and mean file (*mean.binaryproto) for caffe computing
#        produce mean file (*mean.npy) for pycaffe

dataset='train'
resize_height=300
resize_width=300
image_dir='./Total_png'
label_file=./"$dataset"_label.dat
lmdb_dir=./"$dataset"_lmdb."$resize_height"h."$resize_width"w

TOOLS='/home/jklhj/pkg/local/caffe/build/tools/'


## make lmdb files from image_dir and "$dataset"_label.dat
test -e "$dataset"_lmdb && "$dataset"_lmdb
GLOG_logtostderr=1 convert_imageset \
       --resize_height="$resize_height" \
       --resize_width="$resize_width" \
       --shuffle \
       "$image_dir"/ \
       "$dataset"_label.dat \
       "$lmdb_dir"

echo 'Make '"$dataset"'_lmdb, done.'


## Compute the mean image from "$dataset"_lmdb
$TOOLS/compute_image_mean  "$lmdb_dir"  ./"$dataset"_mean.binaryproto

echo 'Make '"$dataset"'_mean.binaryproto, done.'


## Transform mean.binaryproto file into mean.npy
python3  /home/jklhj/bin/caffe/python/mean_bin-npy_convert.py  ./"$dataset"_mean.binaryproto  ./"$dataset"_mean.npy

echo 'Make '"$dataset"'_mean.npy, done.'
