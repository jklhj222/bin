#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

#EXAMPLE=examples/imagenet
#DATA=data/ilsvrc12
#TOOLS=build/tools
EXAMPLE=.
DATA=.
TOOLS=/home/jklhj/pkg/local/caffe/build/tools
dataset=train

$TOOLS/compute_image_mean $EXAMPLE/"$dataset"_lmdb \
  $DATA/"$dataset"_mean.binaryproto

echo "Done."
