#!/bin/bash

#/home/hugh/pkg/local/darknet/darknet detector train ./micplug.data ./micplug03.cfg -gpus 1
/home/hugh/pkg/local/darknet/darknet detector train cfg/adat.data  cfg/adat00.cfg  tiny8_416.conv.12  -gpus 0,1
