#!/usr/bin/env python3

from glob import glob
import os
from PIL import Image
import shutil

def yolo_cut(img_dir, label_dir, obj_file):
    if not os.path.isdir('cut'):
        os.mkdir('cut')
    else:
        shutil.rmtree('cut')
        os.mkdir('cut')

    with open(obj_file, 'r') as f:
        objs = {str(idx):obj.split('\n')[0] 
                  for idx, obj in enumerate(f.readlines())}

        for obj in objs.values():
            if not os.path.isdir('cut/' + obj):
                os.mkdir('cut/' + obj)
            else:
                shutil.rmtree('cut/' + obj)

    img_files = glob(img_dir + '/*')
    print(img_files)

    file_names = list(map(lambda x: os.path.basename(x), img_files))
    print(file_names, '\n')
    print('total files: ', len(file_names))

    num_obj = 0 
    for i, img_file in enumerate(img_files):
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

        img = Image.open(img_file)
        img_width, img_height = img.size

        label_file = os.path.join(label_dir, file_name + '.txt')

        with open(label_file, 'r') as f:
           lines = f.readlines()
        
        for idx, obj in enumerate(lines):
            clas = obj.split(' ')[0]
            cx   = float(obj.split(' ')[1])
            cy   = float(obj.split(' ')[2])
            w    = float(obj.split(' ')[3])
            h    = float(obj.split(' ')[4].split('\n')[0])

            img_cut = img.crop( ((cx-w/2.0)*img_width, 
                                 (cy-h/2.0)*img_height,
                                 (cx+w/2.0)*img_width,
                                 (cy+h/2.0)*img_height) )

            cut_files_dir = os.path.join('./cut', objs[clas])
#            print('cut' + str(idx))

            img_cut.save(os.path.join(cut_files_dir, 
                                      file_name + '_' + 
                                      clas + '.' +
                                      str(idx) + '.' + 
                                      ext) )
            num_obj += 1

        if i+1 == len(file_names):
            print('{}/{} {} {} images'.format(i+1, len(file_names), 
                                              label_file, num_obj), end='\n')

        else:
            print('{}/{} {} {} images'.format(i+1, len(file_names), 
                                              label_file, num_obj), end='\r')

if __name__ == '__main__':
   yolo_cut('./images', './labels', 'obj.names') 
