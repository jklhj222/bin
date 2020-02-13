#!/bin/bash

# $1: input video
# $2: output video

ffmpeg -i "$1" -ss 00:01:34 -to 00:03:48 -c copy "$2"
