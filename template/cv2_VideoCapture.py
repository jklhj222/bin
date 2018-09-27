#!/usr/bin/env python3
""" Created on Wed Sep 26 14:38:45 2018 @author: jklhj """

import cv2

vc = cv2.VideoCapture('00139.MTS')

#print('./images/' + str(c))

c = 0
if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
vc.release()
vc = cv2.VideoCapture('00139.MTS')
while rval:
    print(c, rval, "test")
    rval, frame = vc.read()
    if rval:
        file_name = './images/frame' + '{:05d}.jpg'.format(c)
        cv2.imwrite(file_name, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    c += 1
#    cv2.waitKey(1)

vc.release()