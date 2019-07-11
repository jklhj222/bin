#!/bin/bash

videoFile='video.avi'
outDir='frames'

ffmpeg -i "$videoFile" "$outDir"'/frames_%05d.jpg'
