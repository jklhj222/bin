#!/usr/bin/env python3

import argparse
import glob
import os
import math

parser = argparse.ArgumentParser()

parser.add_argument('--img_dirs', 
                    default=None, 
                    help='ex.: ["dis10", "dis20", "dis30"]')
parser.add_argument('--test_string', default=None, help='ex.: "0123456789"')
parser.add_argument('--sub_min', default=2, help='default: 2')
parser.add_argument('--perfect_score_min', default=5, help='default: 5')
parser.add_argument('--score_type', 
                    default='length_exp', 
                    help='"length_exp" or "length",  default: "length_exp"')

args = parser.parse_args()

img_dirs = eval(args.img_dirs)
test_string = args.test_string
sub_min = int(args.sub_min)
perfect_score_min = int(args.perfect_score_min)
score_type = args.score_type

def sub_strings(test_string, sub_min):
    strings = []
    for i in range(len(test_string)):
        if i>0: test_string = test_string[1:]

        str_tmp = ''
        for char in test_string:

            str_tmp += char

            if len(str_tmp) >= sub_min: strings.append(str_tmp)

    return list(set(strings))


def remove_line(strings, input_list):
    for string in strings:
        while string in input_list:
            input_list.remove(string)


def perfect_score(string_len):
    score = 0.0
    for i in range(string_len-1):
#        print('line_len:', len(string))
#        print('i: ', i, score)
        if score_type == 'length_exp':
            score += math.exp(string_len-i) * (i+1)
        elif score_type == 'length':
            score += (string_len-i) * (i+1)

    return score

def calc_line_score(line, test_strings):
    from math import exp 
    test_line = line.replace(' ', '')[:-1]

    score = 0.0 
    for string in test_strings:
        if string in test_line:
            if score_type == 'length_exp':
                score += exp(len(string))
            elif score_type == 'length':
                score += len(string)

    return score


def calc_grid_score(file_path, test_strings):
    with open(file_path) as f:
        lines = f.readlines()

        remove_line(['\n', ' \n', '  \n', '   \n', '    \n'], lines)

        score = 0.0
        for line in lines:
             line_score = calc_line_score(line, test_strings)
             print(line_score)
             score += line_score

    return score


def grid_effective_LineChar(file_path, test_strings, min_score):
    with open(file_path) as f:
        lines = f.readlines()

        remove_line(['\n', ' \n', '  \n', '   \n', '    \n'], lines)

        num_line = 0
        num_chars = 0
        for line in lines:
            test_line = line.replace(' ', '')[:-1]
            if calc_line_score(test_line, test_strings) > min_score:
                num_line += 1
                num_chars = max(len(test_line), num_chars)
#                print(test_line)

    return num_line, num_chars

strings = sub_strings(test_string, sub_min)

for img_dir in img_dirs:
#    dis = img_dir.split('dis')[1]

    files = glob.glob(img_dir + '/*output.txt')

    ncols = int(math.sqrt(len(files)))
    nrows = math.ceil(len(files) / ncols)
    print('ncols:', ncols, 'nrows:', nrows)

    files  = []
    max_chars = 0
    max_lines = 0
    for row in range(nrows):
        for col in range(ncols):
#            file_name = 'dis' + str(dis) + '_font3_' + str(row) + \
#                        '_' + str(col) + '_output.txt'
            file_name = str(col) + '_' + str(row) + '_output.txt'


            file_path = os.path.join(img_dir, file_name)
            files.append(file_path)           
 
            num_lines, num_chars = grid_effective_LineChar(
                                     file_path, 
                                     strings, 
                                     perfect_score(perfect_score_min) )

            max_lines = max(num_lines, max_lines)
            max_chars = max(num_chars, max_chars)

#            print(file_path, max_lines, max_chars)

    print('max_lines', max_lines)
    print('max_chars', max_chars)

    max_perfect_score = perfect_score(max_chars)

    grid_scores = []
    norm_scores = []
    for row in range(nrows):
        for col in range(ncols):
#            print(file_path, max_lines, max_chars)
#            file_name = 'dis' + str(dis) + '_font3_' + str(row) + \
#                        '_' + str(col) + '_output.txt'
            file_name =  str(col) + '_' + str(row) + '_output.txt'
            
            file_path = os.path.join(img_dir, file_name)

            eff_lines, eff_chars = grid_effective_LineChar(
                                     file_path, 
                                     strings, 
                                     perfect_score(perfect_score_min) )
#            print(file_path)
#            print(eff_lines, eff_chars)

            if eff_lines != 0 and eff_chars !=0:
                grid_score = calc_grid_score(file_path, strings)
                norm_score = grid_score / (perfect_score(eff_chars)*max_lines)

            else:
                grid_score = 0.0
                norm_score = 0.0
               
            grid_scores.append(grid_score)
            norm_scores.append(norm_score)


    print('test3.1:', max(grid_scores), len(grid_scores))
    print('test3.2:', max(norm_scores), min(norm_scores), len(norm_scores))
    print('test3.3:', files[norm_scores.index(max(norm_scores))])
    print()

if os.path.isfile('all_scores.txt'):
    os.remove('all_scores.txt')
for idx, norm_score in enumerate(norm_scores):
    print(idx, files[idx], grid_scores[idx], norm_score)

    col = int(files[idx].split('_')[0].split('/')[1])
    row = int(files[idx].split('_')[1])*-1

    with open('all_scores.txt', 'a') as f:
        if col == ncols-1:
            f.write('{}   {}   {}\n'.format(col, row, norm_score))
            f.write('\n')
        else:
            f.write('{}   {}   {}\n'.format(col, row, norm_score))

    file_prefix = files[idx].split('.txt')[0]
    with open(file_prefix + '_Score.txt', 'w') as f:
        f.write(str(grid_scores[idx]) + ',' +  str(norm_score))












