#!/usr/bin/env python3

import argparse
import glob
import os
import cv2
from statistics import mean 
from sklearn.cluster import KMeans
import numpy as np

#resize = 416
#n_clusters=3

parser = argparse.ArgumentParser()

# global parameters
parser.add_argument('--yolo_size', default=416, help='default: 416')

parser.add_argument('--n_clusters', default=3, help='default: 3')

parser.add_argument('--img_type', default='jpg', help='default: jpg')

subparsers = parser.add_subparsers(dest='subparsers', help='from_dir, from_train_file')

# parameters for directory calculation
parser_dir = subparsers.add_parser('from_dir')

parser_dir.add_argument('--img_dir', default='./images')
parser_dir.add_argument('--label_dir', default='./images')

# parameters for training file
parser_file = subparsers.add_parser('from_train_file')

parser_file.add_argument('--train_file')

args = parser.parse_args()

if args.subparsers == 'from_dir':
#    imgs = glob.glob(os.path.join(args.img_dir, '*.' + args.img_type))
    imgs = glob.glob(os.path.join(args.img_dir, '*'))
    labels = glob.glob(os.path.join(args.label_dir, '*.txt'))

if args.subparsers == 'from_train_file':
    with open(args.train_file) as f:
        imgs = f.readlines()

        imgs = list(map(lambda x: x.replace('\n', ''), imgs))

        labels = []
        for img in imgs:
            if img.endswith('.jpg'):
                labels.append(img.split('.jpg')[0] + '.txt')

            elif img.endswith('.jpeg'):
                labels.append(img.split('.jpeg')[0] + '.txt')

            elif img.endswith('.png'):
                labels.append(img.split('.png')[0] + '.txt')

#        labels = list(map(lambda x: x.split('.' + args.img_type)[0] + '.txt', imgs))

print('imgs: ', len(imgs), len(labels))

#height, width, channel = cv2.imread(imgs[0]).shape

#resize_ratio_w = width / args.resize
#resize_ratio_h = height / args.resize

boxes = []
#anchor_ws = []
#anchor_hs = []
for img, label in zip(imgs, labels):
    height, width, channel = cv2.imread(img).shape

    resize_ratio_w = width / int(args.yolo_size)
    resize_ratio_h = height / int(args.yolo_size)

    with open(label) as f:
        objs = f.readlines()

    for obj in objs:
        clas, cx, cy, w, h = obj.split()

        anchor_w = float(w)*width / resize_ratio_w
        anchor_h = float(h)*height / resize_ratio_h

        area = float(w)*float(h)*width*height/resize_ratio_w/resize_ratio_h

#        boxes.append((anchor_ws, anchor_hs))
        boxes.append((anchor_w, anchor_h))
#        anchor_ws.append(anchor_w)
#        anchor_hs.append(anchor_h)


boxes = np.array(boxes)
#print(boxes, type(boxes), boxes.shape)

kmeans = KMeans(n_clusters=int(args.n_clusters))
kmeans_fit = kmeans.fit(boxes)

label_group = kmeans_fit.labels_

print('test: ', kmeans_fit.labels_, kmeans_fit.labels_.shape)

#print(np.where(label_group==0), len(np.where(label_group==0)[0]))
#print(np.where(label_group==1), len(np.where(label_group==1)[0]))

#print(boxes[label_group==0], boxes[label_group==0].shape)
#print(boxes[label_group==1], boxes[label_group==1].shape)
#print(boxes[label_group==2], boxes[label_group==2].shape)
print()

grps = []
grps_dict = {}
for idx_grp in range(int(args.n_clusters)):
    grps.append(boxes[label_group==idx_grp])

    print('Group {}: {} {:.2f} {}'.format(idx_grp, 
                                        np.mean(grps[idx_grp], axis=0),
                                        np.mean(np.mean(grps[idx_grp], axis=0)),
                                        boxes[label_group==idx_grp].shape))

    grps_dict['Group_{}'.format(idx_grp)] =  ( np.mean(grps[idx_grp], axis=0),
                                               np.mean(np.mean(grps[idx_grp], axis=0)),
                                               boxes[label_group==idx_grp].shape )

    grps_tuple = sorted(grps_dict.items(), key=lambda x: x[1][1])

print()
abox_string = ''
for idx, grps in enumerate(grps_tuple):
    print(grps, grps[1][0][0], )
   
    if idx != len(grps_tuple)-1:
        abox_string += str(int(grps[1][0][0])) + ',' + str(int(grps[1][0][1])) + ', '
    else:
        abox_string += str(int(grps[1][0][0])) + ',' + str(int(grps[1][0][1])) 
       

print()
print('yolo anchor boxes ({} boxes): \n{}'.format(len(grps_tuple) , abox_string))
#    print('Group', idx_grp, ':', np.mean(grps[idx_grp], axis=0), 
#                                 np.mean(np.mean(grps[idx_grp], axis=0)),
#                                 boxes[label_group==idx_grp].shape)
#print(np.mean(grps[0], axis=0), 
#      np.mean(grps[1], axis=0), 
#      np.mean(grps[2], axis=0))
#print(boxes[np.array([433, 432, 431, 430, 429, 428, 427])])

#print(mean(anchor_ws), mean(anchor_hs))


#print(objs, height, width)
#print(labels, height, width)

