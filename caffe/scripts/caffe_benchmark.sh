#/bin/bash

caffe time --model resnet_50.prototxt --iterations 10 --gpu 1
caffe time --model resnet_50.prototxt --weights resnet_50_iter_100000.caffemodel --gpu 1 --iterations 10

