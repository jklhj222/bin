#!/bin/bash

#ffmpeg -i "concat:input1.mp4|input2.mp4|input3.mp4" -c copy output.mp4
ffmpeg -i "concat:input1.mp4|input2.mp4" -c copy output.mp4

