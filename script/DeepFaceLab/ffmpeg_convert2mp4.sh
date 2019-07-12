#!/bin/bash

imgDir='data_dst/merged'
refVideo='ADN-176_cut.mp4'
outVideo='result.mp4'

ffmpeg  -r  2997/100  -i  "$imgDir"'/%5d.png'  -i "$refVideo" -map 0 -map 1:1 -ar 48000 -b:a 192k -b:v 16M -c:a aac -c:v libx264 -pix_fmt yuv420p -strict -2 "$outVideo" 
