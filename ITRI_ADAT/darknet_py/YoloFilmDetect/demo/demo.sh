#!/bin/bash

read -p 'path of video file : ' filename

#/home/hugh/pkg/local/darknet/darknet detector demo  cfg/adat.data cfg/adat00.cfg ./adat00.backup $filename
/home/jklhj/pkg/local/darknet/darknet detector demo  cfg/adat.data cfg/adat00.cfg ./adat00.weights $filename
