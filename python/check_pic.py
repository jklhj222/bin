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

pic_dir = './train_pic'

dir_list = os.listdir("./train_pic")
for i in dir_list:
    test = is_valid_image('./train_pic/' + i)
    if test == False:
        print(i, test)
