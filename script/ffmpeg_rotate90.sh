#!/bin/bash

ffmpeg -i "$1" -vf "transpose=2, transpose=2, transpose=2, transpose=2" -strict -2 "$2"
