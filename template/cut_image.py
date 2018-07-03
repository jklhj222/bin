#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 15:03:28 2018 @author: jklhj
"""

import cv2
import argparse

# 构造参数解析器
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

#print(args)

# 加载图像并显示
image = cv2.imread(args["image"])
cv2.imshow("Original", image)

# 第一次尝试把嘴的部位裁剪出来
mouth = image[85:250, 85:220]
cv2.imshow("Mouth1", mouth)
cv2.waitKey(0)

# 第二次尝试把嘴的部位裁剪出来
mouth = image[85:350, 285:420]
cv2.imshow("Mouth2", mouth)
cv2.waitKey(0)

# 第三次尝试把嘴的部位裁剪出来
mouth = image[85:250, 85:220]
cv2.imshow("Mouth3", mouth)
cv2.waitKey(0)