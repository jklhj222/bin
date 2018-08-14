#/bin/bash

caffe test --model resnet_50.prototxt --weights resnet_50_iter_100000.caffemodel --gpu 1 --iterations 100
