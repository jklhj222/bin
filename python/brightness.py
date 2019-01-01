#!/usr/bin/env python3
""" Created on Tue Jan  1 14:49:02 2019@author: jklhj """

import cv2

img_file = input('the ipnut iamge file name: ')
out_img = input('the output image file: ')
bright_percent = 0.7

img = cv2.imread(img_file)
img[..., 0] = img[..., 0]*bright_percent
img[..., 1] = img[..., 1]*bright_percent
img[..., 2] = img[..., 2]*bright_percent
print(img[..., 1].shape)

#cv2.imshow('img', img)
cv2.imwrite(out_img, img)