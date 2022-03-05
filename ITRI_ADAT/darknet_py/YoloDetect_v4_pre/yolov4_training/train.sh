#!/bin/bash

mkdir backup
#/home/hugh/pkg/local/darknet/darknet detector train ./micplug.data ./micplug03.cfg -gpus 1
#/home/hugh/pkg/local/darknet/darknet detector train cfg/adat.data  cfg/adat00.cfg  tiny8_416.conv.12  -gpus 0,1
#/home/jklhj/pkg/local/darknet_AlexeyAB_cuda10/darknet detector train cfg/adat.data  cfg/yolov3.cfg yolov3.extraction81.weights -map  -dont_show  -gpus 0
/home/hugh/pkg/local/darknet_alexyab_20200825_new/darknet detector train task.data train.cfg -map  -dont_show -gpus 0,1

sed '2,3d' train.cfg | sed '1a batch = 1' | sed '2a subdivisions = 1' > test.cfg
mkdir result
cp backup/train_best.weights test.cfg label.names task.data   result
