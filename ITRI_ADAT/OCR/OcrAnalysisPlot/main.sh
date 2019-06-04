#!/bin/bash

img_file='dis10_H31_L15_201904191516_四LED管_front_aria_font3_bold_best_focus.jpg'
divide_num=15
test_string='01234567890123456789012345678900123456789012345678901234567890'
score_type='length'
perfect_score_min=3
file_ext='jpg'

#1
python3 split_pic.py --img_file "$img_file" --divide_num "$divide_num"
#2
bash tesseract_test.sh
#3
python3 OCR_score.py --img_dirs "['split']" --test_string "$test_string" --score_type "$score_type" --perfect_score_min "$perfect_score_min"
#4
python3 OCR_test_plot.py --img_dir split --file_ext "$file_ext"

