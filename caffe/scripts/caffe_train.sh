#!/bin/bash

caffe train --solver ./resnet_50_solver.prototxt --gpu 1
#caffe train --solver ./resnet_50_solver.prototxt --weights  ./resnet_50_iter_100000.caffemodel --gpu 1
#caffe train --solver ./resnet_50_solver.prototxt --snapshot ./resnet_50_iter_100000.solverstate --gpu 1
