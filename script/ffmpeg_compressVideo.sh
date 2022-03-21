#!/bin/bash

# to avi
#/usr/bin/ffmpeg -i "$1" -vcodec libx265 -crf 25 "$2"

# to mp4
ffmpeg -i "$1" -vcodec h264 -acodec mp2 "$2"
