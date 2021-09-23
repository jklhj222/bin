#!/usr/bin/env python3

import cv2
import numpy as np

toSize_width = 720
toSize_height = 1055

img = cv2.imread('yieldstar.jpg')

img_height, img_width = img.shape[:2]

print(img_height,img_width)

#
points1 = np.float32([[0, 131], [1567, 170], [160, 2200], [1455, 2165]])
points2 = np.float32([[0,0], [toSize_width,0], [0,toSize_height], [toSize_width,toSize_height]])

# get transform matrix
M = cv2.getPerspectiveTransform(points1, points2)

# perspective
processed = cv2.warpPerspective(img,M,(toSize_width, toSize_height))

#cv2.imshow("org",img)
cv2.imshow("processed",processed)

cv2.imwrite('yieldstar_crop_perspect.jpg', processed)

cv2.waitKey(0)

