#!/usr/bin/env python3
""" Created on Sat Jul 14 00:55:31 2018 author: jklhj """

import os
import shutil
from collections import defaultdict
from PIL import Image
import random
from math import floor

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
            file_cut.append(fullpath.split('.JPG')[0][:-1])

index_file_cut = []
for index, name in enumerate(file_cut):
    index_file_cut.append([index, name])
    
index_file_path = []
for index, name in enumerate(file_path):
    index_file_path.append([index, name])
    
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)


def cut_img(src_img_path, dst_img_dir, x, y, xw, yh):
    img = Image.open(src_img_path)
    region = img.crop( (x, y, xw, yh) )
    
    cut_pic = src_img_path.split('/')[-1].split('.')[0] + '_' \
                       + str(xw - x) + 'x.' + str(yh - y) + 'y.JPG'
        
    region.save(dst_img_dir + cut_pic)

    return img.size, region.size

repeat_pic = []
source = file_cut
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
            cut_img(pics[i], './data_before/', cut_x, cut_y, cut_xw, cut_yh)
            
        elif i+1 == len(pics) and len(pics)>1:
            print("index last: ", pics[i])
#            shutil.copy( pics[i], './data_after')            
            cut_img(pics[i], './data_after/', cut_x, cut_y, cut_xw, cut_yh)

        else:
            print("index else: ", pics[i])
#            shutil.copy( pics[i], './data_middle')
            cut_img(pics[i], './data_middle/', cut_x, cut_y, cut_xw, cut_yh)

print(len(file_path), len(repeat_pic))

divide_percent = 0.9

for dir_name in ['data_after', 'data_before', 'data_middle']:    
    files = os.listdir(dir_name)
    
    train_files = random.sample( files, floor(len(files)*divide_percent) )
    
    val_files = list(set(files) - set(train_files))
   
    os.makedirs( os.path.join(dir_name, 'train') )
    os.makedirs( os.path.join(dir_name, 'val') )

    for train_file in train_files:
        shutil.move( os.path.join(dir_name, train_file), 
                     os.path.join(dir_name, 'train') )
    
    for val_file in val_files:
        shutil.move( os.path.join(dir_name, val_file), 
                     os.path.join(dir_name, 'val') )
    
    