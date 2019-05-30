#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import glob
import argparse
import math
import os

parser = argparse.ArgumentParser()

parser.add_argument('--img_dir', default=None)
parser.add_argument('--out_file', default='test.png')
parser.add_argument('--file_ext', default=None, help='jpg, png or ...')
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
ext_name = args.file_ext

files = glob.glob(img_dir + '/*.' + ext_name)

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
#        idx_subfig = nrows * col + (row+1)
        print('idx_subfig:', idx_subfig, 'ncols:', ncols, 'row:', row, 'col:', col)
        sub_figs.append(fig.add_subplot(nrows, ncols, idx_subfig, 
                                        xticks=[], yticks=[]))
   
#        file_name = 'dis' + str(dis) + '_font3_' + str(row) + \
#                    '_' + str(col) + '_output.txt'
        file_name = str(col) + '_' + str(row) + '_output.txt'
        file_path = os.path.join(img_dir, file_name)

        score_file = str(col) + '_' + str(row) + '_output_Score.txt'
        score_file_path = os.path.join(img_dir, score_file)

        output_string = ''
        with open(file_path) as f:
            for line in f.readlines():
                output_string += line
       
        with open(score_file_path) as f:
            score, norm_score = f.readline().split(',')

        grid = '(' + str(col) + ',' + str(row) + ')'

        img = Image.new('RGB', subfig_size, color = (255, 255, 255))
        font_type = 'NotoSansCJK-Medium.ttc'
        font_out = ImageFont.truetype(font_type, 10, encoding='utf-8') 
        font_grid = ImageFont.truetype(font_type, 15, encoding='utf-8') 

        d = ImageDraw.Draw(img)

        if row == int(nrows/2) and col == int(ncols/2):
            d.text((10,10), 
                   grid + ' center' + ' {:.4f}'.format(float(norm_score)),
                   fill=(0,0,255), font=font_grid)
        else:
            d.text((10,10), grid + ' {:.4f}'.format(float(norm_score)), 
                   fill=(255,0,0), font=font_grid)

        d.text((10,30), output_string, fill=(0,0,0), font=font_out)
#       d.text((10,10), "Hello World\n damn world", (255,255, 255))
        sub_figs[idx_subfig-1].imshow(img)

plt.savefig(args.out_file, bbox_inches='tight')
if args.show: plt.show() 

