#!/usr/bin/env python3

import argparse
import os
import math

parser = argparse.ArgumentParser()

parser.add_argument('--test_file')
parser.add_argument('--test_string', default=None, help='ex.: "0123456789"')

args = parser.parse_args()

test_file = args.test_file
test_string = args.test_string

sub_min = 2 

def sub_strings(test_string, sub_min):
    strings = []
    for i in range(len(test_string)):
        if i>0: test_string = test_string[1:]

        str_tmp = ''
        for char in test_string:

            str_tmp += char

            if len(str_tmp) >= sub_min: strings.append(str_tmp)

    return list(set(strings))
#    return list(strings)


def remove_line(strings, input_list):
    for string in strings:
        while string in input_list:
            input_list.remove(string)


def perfect_score(string_len):
    score = 0.0
    for i in range(string_len-1):
#        print('line_len:', len(string))
#        print('i: ', i, score)
        score += math.exp(string_len-i) * (i+1)

    return score


def calc_line_score(line, test_strings):
    from math import exp
    test_line = line.replace(' ', '')[:-1]

    score = 0.0
    for string in test_strings:
        if string in test_line:
            score += exp(len(string))

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

        num_lines = 0    
        num_chars = 0
        for line in lines:
            test_line = line.replace(' ', '')[:-1]    
            if calc_line_score(test_line, test_strings) > min_score:
                num_lines += 1
                num_chars = max(len(test_line), num_chars)
                print(test_line)              

    return num_lines, num_chars



strings = sub_strings(test_string, sub_min)
#print(strings, len(strings), strings[100])

grid_score = calc_grid_score(test_file, strings)

num_line, num_chars = grid_effective_LineChar(test_file, strings, perfect_score(4))
print("line, chars: ", num_line, num_chars)

max_perfect_score = perfect_score(num_chars)
print('max_perfect_score: ', max_perfect_score)

norm_score = grid_score / (max_perfect_score*num_line)
print('norm_score: ', norm_score)

