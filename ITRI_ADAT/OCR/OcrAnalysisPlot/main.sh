#!/bin/bash

img_file='new9.bmp'
divide_num=15
test_string='0123456789012345678901234567890'
score_type='length'
perfect_score_min=3

#1
python3 split_pic.py --img_file "$img_file" --divide_num "$divide_num"
#2
bash tesseract_test.sh
#3
python3 OCR_score.py --img_dirs "['split']" --test_string "$test_string" --score_type "$score_type" --perfect_score_min "$perfect_score_min"
#4
python3 OCR_test_plot.py --img_dir split

