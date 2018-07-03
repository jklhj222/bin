#!/bin/bash
# 20180506, to extarct the features of caffemodel

MODEL='./caffe_alexnet_train_iter_410000.caffemodel'
WEIGHTS='./train_val.prototxt'
LAYER='fc7'
FEATURE_SAVE='./features/'"$LAYER"
NUM_MINI_BATCH=1
DB_TYPE='lmdb'
CGPU='GPU'

test -e ./features || mkdir ./features
test -e $FEATURE_SAVE && rm -r $FEATURE_SAVE

extract_features  "$MODEL"  "$WEIGHTS"  "$LAYER"  "$FEATURE_SAVE"  "$NUM_MINI_BATCH"  "$DB_TYPE"  "$CGPU"
