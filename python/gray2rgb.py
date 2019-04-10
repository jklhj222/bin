#!/usr/bin/env python3
""" Created on Wed Apr  3 14:54:28 2019 @author: jklhj """

import cv2
import os

file_list = os.listdir('test_images')

for i in file_list:
    src_path = os.path.join('test_images', i)
    dst_path = os.path.join('test_images_rgb', i)
    img = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
#    img = cv2.imread('test_05629.png', cv2.IMREAD_UNCHANGED)

    backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    cv2.imwrite(dst_path, backtorgb)


