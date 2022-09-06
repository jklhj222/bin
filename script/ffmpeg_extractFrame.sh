#!/bin/bash

videoFile='video.avi'
outDir='frames'

# -qscale normal range for JPEG is 2-31 with 31 being the worst quality.
ffmpeg -i "$videoFile" -qscale:v 2 "$outDir"'/frames_%05d.jpg'
