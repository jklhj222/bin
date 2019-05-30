#!/usr/bin/env python3
""" Created on Wed May 15 13:15:19 2019 @author: jklhj """
import argparse
from PIL import Image, ImageDraw, ImageFont
import os

parser = argparse.ArgumentParser()

parser.add_argument('--img_file', default=None)
parser.add_argument('--divide_num', default=15)

args = parser.parse_args()

img_file = args.img_file
if 'jpg' in img_file: 
    file_name = img_file.split('.jpg')[0]
    ext_name = 'jpg'
if 'png' in img_file: 
    file_name = img_file.split('.png')[0]
    ext_name = 'png'

divide_num = int(args.divide_num)

img = Image.open(img_file)
img_RGB = img.convert('RGB')
img_d = ImageDraw.Draw(img_RGB)

width, height = img.size

print(img.size, width, height)

width_interval  = int(width/divide_num)
height_interval = int(height/divide_num)
print(width_interval, height_interval)

if not os.path.isdir('split'):
    os.mkdir('split')

font_type = 'NotoSansCJK-Medium.ttc'
font_grid = ImageFont.truetype(font_type, 25, encoding='utf-8')

for i in range(divide_num+1):

    img_d.line( ((i*width_interval, 0),
                 (i*width_interval, height)), 
                (255, 0, 0),
                width=5 )

    img_d.line( ((0, i*height_interval),
                 (width, i*height_interval)), 
                (255, 0, 0), 
                width=5 )

for i in range(divide_num):
    for j in range(divide_num):
        img2 = img.crop( (i*width_interval, j*height_interval, 
                          (i+1)*width_interval, (j+1)*height_interval) )

        img_d.text((i*width_interval+10, j*height_interval+10), 
                   str(i) + '_' + str(j), 
                   fill=(255, 0, 0), font=font_grid)

        print(i*width_interval, j*height_interval, 
              (i+1)*width_interval, (j+1)*height_interval)

        img2.save('split/' + str(i) + '_' + str(j) + '.' + ext_name)

img_RGB.save(file_name + '_grid.' + ext_name)
  
