#!/bin/bash

#/home/hugh/pkg/local/darknet_alexyab_20200825_new/darknet detector train task.data train.cfg -map  -dont_show -gpus 0,1
darknet_path='/home/jklhj/pkg/local/darknet_yolo_v4_pre/darknet'

echo `date` > elapsed_time.dat

mkdir backup

nclass=`wc label.names | awk '{print $1}'`
arch=`grep arch task.data | awk -F '=' '{print $2}'`
filter=`echo "($nclass + 5) * 3"  | bc`
echo arch: $arch

if [ $arch = 'yolov4' ]
then
    echo in yolov4
    cp yolov4.cfg train.cfg
    nfilter1=`echo $(grep -n yolo train.cfg | head -1 | awk -F ':' '{print $1}') - 3 | bc`
    nfilter2=`echo $(grep -n yolo train.cfg | head -2 | tail -1 | awk -F ':' '{print $1}') - 3 | bc`
    nfilter3=`echo $(grep -n yolo train.cfg | tail -1 | awk -F ':' '{print $1}') - 3 | bc`
    sed -i "$nfilter1""cfilters = $filter" train.cfg
    sed -i "$nfilter2""cfilters = $filter" train.cfg
    sed -i "$nfilter3""cfilters = $filter" train.cfg
elif [ $arch = 'yolov4-tiny' ]
then
    echo in yolov4-tiny
    cp yolov4-tiny.cfg train.cfg
    nfilter1=`echo $(grep -n yolo train.cfg | head -1 | awk -F ':' '{print $1}') - 3 | bc`
    nfilter2=`echo $(grep -n yolo train.cfg | tail -1 | awk -F ':' '{print $1}') - 3 | bc`
    sed -i "$nfilter1""cfilters = $filter" train.cfg
    sed -i "$nfilter2""cfilters = $filter" train.cfg
fi

sed -i 's/classes.*$/classes = '"$nclass"'/g' train.cfg
sed -i 's/classes.*$/classes='"$nclass"'/g' task.data 

"$darknet_path" detector train task.data train.cfg -map  -dont_show -gpus 0

sed '2,3d' train.cfg | sed '1a batch = 1' | sed '2a subdivisions = 1' > test.cfg

mkdir result
cp backup/train_best.weights test.cfg label.names task.data   result

echo `date` >> elapsed_time.dat
