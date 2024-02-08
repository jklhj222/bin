#!/usr/bin/env python3

import os
from PIL import Image

def is_jpeg(file_path):
    return file_path.lower().endswith(('.jpg', '.jpeg'))

def is_jpeg_corrupted(file_path):
    try:
        img = Image.open(file_path)
        img.verify() 
        return False 
    except (IOError, SyntaxError):
        return True 

def check_jpeg_files(directory):
    idx = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_jpeg(file_path):
                if is_jpeg_corrupted(file_path):
                    print(f"{idx} GOOD: {file_path}")
#                else:
#                    print(f"{idx} BAD: {file_path}")

                idx += 1

directory = '.'  # current directory
check_jpeg_files(directory)

