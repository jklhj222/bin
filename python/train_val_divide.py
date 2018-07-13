#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:00:51 2018  jklhj
ver. 1.0.0
"""

import random
import os
import shutil
from math import floor

srcDir = './train'
DividePercent = 0.8

def random_select(srcDir, DividePercent):
    if os.path.exists(os.path.join(srcDir, "train_data")):
        shutil.rmtree(os.path.join(srcDir, "train_data"))
    if os.path.exists(os.path.join(srcDir, "val_data")):
        shutil.rmtree(os.path.join(srcDir, "val_data"))

    dir_list = os.listdir(srcDir) 
    for subdir in dir_list:
        print(subdir)
        file_list = os.listdir( os.path.join(srcDir, subdir) )
        file_number = len(file_list)
        divide_number = floor(file_number * DividePercent)
        train_file = random.sample(file_list, divide_number)        
#        val_file = list(set(file_list).difference(set(train_file)))
        val_file = list(set(file_list) - set(train_file))
            
        if not os.path.exists(os.path.join(srcDir, "train_data", subdir)):
            os.makedirs(os.path.join(srcDir, "train_data", subdir))
            
        for file in train_file:
            shutil.copy(os.path.join(srcDir, subdir, file),
                        os.path.join(srcDir, "train_data", subdir, file) )

        if not os.path.exists(os.path.join(srcDir, "val_data", subdir)):
            os.makedirs(os.path.join(srcDir, "val_data", subdir))
            
        for file in val_file:
            shutil.copy(os.path.join(srcDir, subdir, file),
                        os.path.join(srcDir, "val_data", subdir, file) )
        
if __name__ == '__main__':        
    random_select(srcDir, DividePercent)
