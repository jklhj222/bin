#!/bin/bash

darknet='/home/hugh/pkg/local/darknet_yolov3_cuda10/darknet'
workdir='./'

num_class=3

cd $workdir
mkdir backup
cp ~/bin/ITRI_ADAT/darknet/train.sh .
cp -r ~/bin/ITRI_ADAT/darknet/cfg .
cp -r ~/bin/ITRI_ADAT/darknet/data .

sed -i 's/num_class/'"$num_class"'/g' cfg/yolov3.cfg
sed -i 's/num_class/'"$num_class"'/g' cfg/adat.data
