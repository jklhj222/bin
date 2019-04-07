#!/bin/bash

/home/hugh/pkg/local/darknet/darknet detector test cfg/adat.data cfg/yolov3.cfg ./yolov3_10000.weights -thresh 0.25
