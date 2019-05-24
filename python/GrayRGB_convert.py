#!/usr/bin/env python3
""" Created on Wed Apr  3 14:54:28 2019 @author: jklhj """

import cv2
from PIL import Image

def gray2rgb(img_file, out_file):
    img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

    back2rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    cv2.imwrite(out_file, back2rgb)

    return back2rgb

def rgb2gray(img_file, out_file):
    img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

    back2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(out_file, back2gray)
    
    return back2gray


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--img_file', default=None)

    parser.add_argument('--out_file', default=None)

    parser.add_argument('--convert_mode', 
                        help='rgb2gray or gray2rgb',
                        default=None)

    args = parser.parse_args()

    if args.convert_mode == 'rgb2gray':
        rgb2gray(args.img_file, args.out_file)

    elif args.convert_mode == 'gray2rgb':
        gray2rgb(args.img_file, args.out_file)

    else:
        print('Nothing happened, wrong parameters.')


