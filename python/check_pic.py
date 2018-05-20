#!/usr/bin/env python3

from PIL import Image
import os

def is_valid_image(filename):
    valid = True
    try:
        Image.open(filename).load()
    except OSError:
        valid = False
    return valid

pic_dir = './validation_pic/'

index = 0
dir_list = os.listdir(pic_dir)
for i in dir_list:
    index += 1
    test = is_valid_image(pic_dir + i)
    if test == False:
        print(i, test)
    if index % 10000 == 0:
        print(index)
