#!/usr/bin/env python3

import dlib
import numpy as np
import cv2
import os
import argparse


print(dlib.DLIB_USE_CUDA)

print(dlib.cuda.get_num_devices())


parser = argparse.ArgumentParser()

parser.add_argument('--img_dir', default=None)
parser.add_argument('--out_dir', default=None)
parser.add_argument('--gpu_idx', default=0)
parser.add_argument('--ext_ratio', 
                    default=0.4, 
                    help='set to extend the bonding box of face, dafault=0.4')
parser.add_argument('--show_img',
                    default=False,
                    help='default: False',
                    action='store_true')

args = parser.parse_args()

image_dir = args.img_dir
out_dir = args.out_dir
ext_ratio = float(args.ext_ratio) / 2.0

dlib.cuda.set_device(int(args.gpu_idx))

detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')

for img_file in os.listdir(image_dir): 
    if '.jpg' in img_file or '.png' in img_file:

        if '.jpg' in img_file:
            filename = img_file.split('.jpg')[0]
        if '.png' in img_file:
            filename = img_file.split('.png')[0]

        print('current image: ', img_file)
        
        img = cv2.imread(os.path.join(image_dir, img_file)) 
        img_bbox = img.copy()

        if img.shape[0]*img.shape[1] > 8000000:             
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

        dets = detector(img, 1)                   #使用檢測運算元檢測人臉，返回的是所有的檢測到的人臉區域

        for k, d in enumerate(dets):
            rec = dlib.rectangle( d.rect.left(),
                                  d.rect.top(),
                                  d.rect.right(),
                                  d.rect.bottom() )

            width = rec.right() - rec.left()
            height = rec.bottom() - rec.top()
           
            ext_left   = int(rec.left() - width*ext_ratio) \
                           if int(rec.left() - width*ext_ratio) > 0 else 1

            ext_right  = int(rec.right() + width*ext_ratio) \
                           if int(rec.right() + width*ext_ratio) \
                           < img.shape[1] else img.shape[1]

            ext_top    = int(rec.top() - height*ext_ratio) \
                           if int(rec.top() - height*ext_ratio) > 0 else 1

            ext_bottom = int(rec.bottom() + height*ext_ratio) \
                           if int(rec.bottom() + height*ext_ratio) \
                           < img.shape[0] else img.shape[0]

            img_cut = img[ext_top:ext_bottom, ext_left:ext_right]

            cv2.imwrite(os.path.join(out_dir, 
                                     filename + '_' + str(k) + '.jpg'), 
                        img_cut)

            if args.show_img:
                cv2.rectangle(img_bbox, 
                              (ext_left, ext_top), 
                              (ext_right, ext_bottom), 
                              (0, 255, 0), 
                              2)   

                text = "{:d}".format(k) 
                cv2.putText(img_bbox, 
                            text, 
                            (ext_right, ext_top), 
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.7, 
                            (255, 255, 255), 
                            1, 
                            cv2.LINE_AA)

        if args.show_img:
            cv2.imshow('image', img_bbox)
            cv2.waitKey(0)

cv2.destroyAllWindows()  
