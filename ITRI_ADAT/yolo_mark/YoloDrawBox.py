#!/usr/bin/env python3

import numpy as np
import os
import cv2
from glob import glob

def draw_box(img_dir, label_dir, save_dir, obj_file):
    with open(obj_file, 'r') as f:
        objs = {idx: obj.split('\n')[0]
                  for idx, obj in enumerate(f.readlines())}

    img_files = glob(img_dir + '/*')
#    print(img_files)
     
    file_names = list(map(lambda x: os.path.basename(x), img_files))
#    print(file_names, '\n')
    print('total files: ', len(file_names))

    for i, img_file in enumerate(img_files):
        print('progress: ', i+1, '/', len(file_names), end='\r')

        if '.jpg' in img_file:
            file_name = os.path.basename(img_file).split('.jpg')[0]
            ext = 'jpg'

        elif '.png' in img_file:
            file_name = os.path.basename(img_file).split('.png')[0]
            ext = 'png'

        elif '.JPG' in img_file:
            file_name = os.path.basename(img_file).split('.JPG')[0]
            ext = 'JPG'

        elif '.PNG' in img_file:
            file_name = os.path.basename(img_file).split('.PNG')[0]
            ext = 'PNG'

        else:
            continue
   
        img = cv2.imread(img_file)
        img_height, img_width = img.shape[0], img.shape[1]

        label_file = os.path.join(label_dir, file_name + '.txt')

        with open(label_file, 'r') as f:
            lines = f.readlines()

        for idx, obj in enumerate(lines):
            clas = obj.split(' ')[0]
            cx   = float(obj.split(' ')[1])
            cy   = float(obj.split(' ')[2])
            w    = float(obj.split(' ')[3])
            h    = float(obj.split(' ')[4].split('\n')[0])

            l    = int((cx - w/2) * img_width)
            r    = int((cx + w/2) * img_width)
            t    = int((cy - h/2) * img_height)
            b    = int((cy + h/2) * img_height)

            cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 5)

            img = cv2.putText(img,
                              objs[int(clas)],
                              (l, t-10),
                              cv2.FONT_HERSHEY_TRIPLEX,
                              1,
                              (0, 255, 0),
                              1,
                              cv2.LINE_AA)

            cv2.imwrite(os.path.join(save_dir, file_name + '.' + ext), img)


if __name__ == '__main__':
    img_dir = 'images'
    label_dir = 'labels'
    output_dir = 'drawBox'
    label_file = 'obj.names'

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    draw_box(img_dir, label_dir, output_dir, label_file)


