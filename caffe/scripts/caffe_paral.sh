#!/bin/bash

caffe train --solver resnet_50_solver.prototxt --gpu 0,1
#caffe train --solver resnet_50_solver.prototxt --gpu all 
