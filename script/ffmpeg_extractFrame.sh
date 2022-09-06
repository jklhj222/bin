#!/bin/bash

videoFile='video.avi'
outDir='frames'

# -qscale normal range for JPEG is 2-31 with 31 being the worst quality.
# You can use a value of 1 but you must add the -qmin 1 output option (because the default is -qmin 2).
ffmpeg -i "$videoFile" -qmin 1 -qscale:v 2 "$outDir"'/frames_%05d.jpg'
