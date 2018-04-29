#!/bin/bash

caffe test --weights=caffe_alexnet_train_iter_100000.caffemodel --model=train_val.prototxt
