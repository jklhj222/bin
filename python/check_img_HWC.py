#!/usr/bin/env python3
""" Created on Mon Oct  8 16:41:05 2018 @author: jklhj """

import cv2
import sys
import argparse

parser = argparse.ArgumentParser(
        description='Check the height, width, channels, and data type of image.')

parser.add_argument('--img_path',
                    default=None,
                    help='the image path to check.')

args = parser.parse_args()

if __name__ == "__main__":
    img = cv2.imread(args.img_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        print("Failed to load image file.")
        sys.exit(1)

    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1

    print("width: " + str(width))
    print("height: " + str(height))
    print("channels: " + str(channels))
    print("dtype: " + str(img.dtype))
