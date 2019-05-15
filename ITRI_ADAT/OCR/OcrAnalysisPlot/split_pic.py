#!/usr/bin/env python3
""" Created on Wed May 15 13:15:19 2019 @author: jklhj """
import argparse
from PIL import Image
import os

parser = argparse.ArgumentParser()

parser.add_argument('--img_file', default=None)
parser.add_argument('--divide_num', default=15)

args = parser.parse_args()

img_file = args.img_file
divide_num = int(args.divide_num)

img = Image.open(img_file)

width, height = img.size

print(img.size, width, height)

width_interval  = int(width/divide_num)
height_interval = int(height/divide_num)
print(width_interval, height_interval)

if not os.path.isdir('split'):
    os.mkdir('split')

for i in range(divide_num):
    for j in range(divide_num):
        img2 = img.crop( (i*width_interval, j*height_interval, 
                          (i+1)*width_interval, (j+1)*height_interval) )


        print(i*width_interval, j*height_interval, 
              (i+1)*width_interval, (j+1)*height_interval)
        img2.save('split/' + str(i) + '_' + str(j) + '.jpg')

