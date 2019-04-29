#!/usr/bin/env python3
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os
import argparse
import glob

parser = argparse.ArgumentParser()

parser.add_argument('--img_dir', default=None)
parser.add_argument('--out_file', default='test.png', help='default: test.png')
parser.add_argument('--img_resol', default=(4032, 3024), help='default: (4032, 3204)')
parser.add_argument('--font_size', default=50, help='default: 50')
parser.add_argument('--box_size', default=(200, 100), help='default: (200, 100)')

args = parser.parse_args()

img_dir = args.img_dir
out_file = args.out_file
img_resol = args.img_resol
font_size = int(args.font_size)
box_size = eval(args.box_size)

files = glob.glob(img_dir + '/*.txt')

img = Image.new('RGB', img_resol, color=(255, 255, 255))

font_type = 'NotoSansCJK-Medium.ttc'
font_out = ImageFont.truetype(font_type, font_size, encoding='utf-8')
d = ImageDraw.Draw(img)

for i in files:
    file_name = os.path.basename(i)
    file_path = i 

    x = int(file_name.split('_')[2]    )
    y = int(file_name.split('_')[3].split('.')[0])
    print(x, y)

    output_string = ''
    with open(file_path) as f:
        for line in f.readlines():
            output_string += line

    d.text((x, y), output_string, fill=(0,0,255), font=font_out)
    d.rectangle(((x-15, y-15), (x+box_size[0], y+box_size[1])), outline='red', width=5)

img.save(out_file)
