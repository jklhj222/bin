#!/usr/bin/env python3
""" Created on Wed Apr  3 14:54:28 2019 @author: jklhj """

import cv2

#img = cv2.imread('Sc_257.bmp')
img = cv2.imread('frames_00370.jpg', 0)

img = cv2.resize(img, (500, 500))



print(img.shape)


blur = cv2.medianBlur(img, 5)

ret, thred = cv2.threshold(blur, 99, 255, cv2.THRESH_BINARY)



cv2.imshow("Original", img)
cv2.imshow("medianBlur", blur)
cv2.imshow("thred", thred)
#
cv2.waitKey(0)  