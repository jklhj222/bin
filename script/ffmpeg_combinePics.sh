#!/bin/bash

ffmpeg -r 10 -i images/frame"%5d.jpg" -r 30 -vf "scale=656:-2" out.mp4
