#!/usr/bin/env python3
""" Created on Sat Jul 14 00:55:31 2018 author: jklhj """

import os
import shutil
from collections import defaultdict
from PIL import Image

for dir_name in ['data_after', 'data_before', 'data_middle']:
    if os.path.exists(os.path.join('./', dir_name)):
        shutil.rmtree(os.path.join('./', dir_name))
    if not os.path.exists(os.path.join('./', dir_name)):
        os.makedirs(os.path.join('./', dir_name))

file_path = []
file_cut = []
for root, dirs, files in os.walk('./'):
    for f in files: 
        fullpath = os.path.join(root, f)
        if fullpath.split('.')[-1] == 'JPG':
            file_path.append(fullpath)
            file_cut.append(fullpath.split('/')[-1]\
                            .split('.')[0][0:-1])

index_file_cut = []
for index, name in enumerate(file_cut):
    index_file_cut.append([index, name])
    
source = file_cut
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

def cut_img(src_img_path, dst_img_path, x, y, xw, yh):
    img = Image.open(src_img_path)
    img_size = img.size
    region = img.crop( (x, y, xw, yh) )
    region.save(dst_img_path)
    
    return img_size

tmpp = list(list_duplicates(source))

repeat_pic = []
for _, index in sorted(list_duplicates(source)):
    repeat_pic.append( sorted([ file_path[i] for i in index ]) )

cut_x = 280
cut_y = 180
cut_xw = 400
cut_yh = 300

for pics in repeat_pic:
    for i in range(len(pics)):
        if i == 0:
            print("index 0: ", pics[i])
#            shutil.copy( pics[i], './data_before')
            cut_pic = pics[i].split('/')[-1].split('.')[0] + '_' \
                       + str(cut_xw-cut_x) + 'x.' + str(cut_yh-cut_y) + 'y.JPG'
            cut_img(pics[i], './data_before/' + cut_pic,
                    cut_x, cut_y, cut_xw, cut_yh)
            
        elif i+1 == len(pics):
            print("index last: ", pics[i])
#            shutil.copy( pics[i], './data_after')            
            cut_pic = pics[i].split('/')[-1].split('.')[0] + '_' \
                       + str(cut_xw-cut_x) + 'x.' + str(cut_yh-cut_y) + 'y.JPG'
            cut_img(pics[i], './data_after/' + cut_pic,
                    cut_x, cut_y, cut_xw, cut_yh)

        else:
            print("index else: ", pics[i])
#            shutil.copy( pics[i], './data_middle')
            cut_pic = pics[i].split('/')[-1].split('.')[0] + '_' \
                       + str(cut_xw-cut_x) + 'x.' + str(cut_yh-cut_y) + 'y.JPG'
            cut_img(pics[i], './data_middle/' + cut_pic,
                    cut_x, cut_y, cut_xw, cut_yh)

print(len(file_path), len(repeat_pic))
