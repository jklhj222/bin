#!/usr/bin/env python3
""" Created on Tue Feb 19 14:36:41 2019 @author: jklhj """

import numpy as np
import cv2
#from PIL import Image, ImageDraw

img = cv2.imread('frame00153.jpg')
#img = np.asarray(Image.open("frame00153.jpg"))
print(type(img), img)
#img = Image.fromarray(np.uint8(img))

cv2.rectangle(img, (100, 100), (500, 500), (0, 255, 0), 2) 
cv2.rectangle(img, (300, 400), (600, 700), (255, 255, 0), 2) 

#draw = ImageDraw.Draw(img)

#draw.rectangle([(100, 100), (500, 500)])

#img.show()
cv2.imshow('test', img)
cv2.waitKey(0)