#!/usr/bin/env python3
import os

def find_matching_txt(file_path):
    file_name = os.path.splitext(file_path)[0]
    txt_file_path = file_name + '.txt'
    if os.path.exists(txt_file_path):
        return txt_file_path
    else:
        return None

def check_matching_txt_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                matching_txt = find_matching_txt(file_path)
#                if matching_txt:
#                    print(f"in {file_path) find matching txt file: {matching_txt}")

                if not matching_txt:
                    print(f"in {file_path} did't find match txt file: {matching_txt}")

directory = '.' 
check_matching_txt_files(directory)
