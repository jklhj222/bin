#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import glob
import argparse
import math

parser = argparse.ArgumentParser()

parser.add_argument('--img_dir', default=None)
parser.add_argument('--out_file', default='test.png')
parser.add_argument('--dis', default=None)
parser.add_argument('--fig_size', default=100, help='default:100')
parser.add_argument('--subfig_size', default=200, help='default:100')
parser.add_argument('--show', default=False,
                              action='store_true')

args = parser.parse_args()

img_dir = args.img_dir
dis = args.dis
fig_size = (int(args.fig_size), int(args.fig_size))
subfig_size = (int(args.subfig_size), int(args.subfig_size))

files = glob.glob(img_dir + '/*.jpg')

ncols = int(math.sqrt(len(files)))
nrows = math.ceil(len(files) / ncols)
print('ncols:', ncols, 'nrows:', nrows)
print('fig_size:', fig_size)
print('subfig_size:', subfig_size)

fig = plt.figure(figsize=fig_size)
fig.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

sub_figs = []
for row in range(nrows):
    for col in range(ncols):
        idx_subfig = ncols * row + (col+1)
        print('idx_subfig:', idx_subfig, 'ncols:', ncols, 'row:', row, 'col:', col)
        sub_figs.append(fig.add_subplot(nrows, ncols, idx_subfig, 
                                        xticks=[], yticks=[]))
   
        file_name = 'dis' + str(dis) + '_font3_' + str(row) + \
                    '_' + str(col) + '_output.txt'

        output_string = ''
        with open(file_name) as f:
            for line in f.readlines():
                output_string += line
       
        grid = '(' + str(col) + ',' + str(row) + ')'

        img = Image.new('RGB', subfig_size, color = (255, 255, 255))
        font_type = 'NotoSansCJK-Medium.ttc'
        font_out = ImageFont.truetype(font_type, 10, encoding='utf-8') 
        font_grid = ImageFont.truetype(font_type, 15, encoding='utf-8') 

        d = ImageDraw.Draw(img)

        if row == int(nrows/2) and col == int(ncols/2):
            d.text((10,10), grid + ' center', fill=(0,0,255), font=font_grid)
        else:
            d.text((10,10), grid, fill=(255,0,0), font=font_grid)
        d.text((10,30), output_string, fill=(0,0,0), font=font_out)
#       d.text((10,10), "Hello World\n damn world", (255,255, 255))
        sub_figs[idx_subfig-1].imshow(img)

plt.savefig(args.out_file, bbox_inches='tight')
if args.show: plt.show() 

