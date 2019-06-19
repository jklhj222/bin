#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--img_file', default=None)

args = parser.parse_args()

# read image file
img = cv2.imread(args.img_file)

# to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# calculate the value of each bin
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
hist = hist.reshape(256)
print(hist, hist.shape, type(hist))

# draw histogram
plt.bar(range(1, 257), hist)
plt.show()
