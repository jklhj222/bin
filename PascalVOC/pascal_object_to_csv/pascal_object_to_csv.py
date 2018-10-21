#!/usr/bin/env python3
""" Created on Fri Oct 19 16:46:31 2018 @author: jklhj """

import xml.etree.cElementTree as ET
import glob
import collections
import csv
import sys

xml_files = glob.glob('./Annotations/*.xml')

file_name_list = list(map(lambda x: x.split('/')[-1].split('.')[0], xml_files))

num = 1
name_object_dict = {}
for file in xml_files:
    tree = ET.ElementTree(file=file)

    root = tree.getroot()
    
    file_name = file.split('/')[-1].split('.')[0]
    
    object_list = []
    for child1 in root:
        if child1.tag == 'object':
            for child2 in child1:
                if child2.tag == 'name':
#                    print(file, child2.text)
                    object_list.append(child2.text)
    
    name_object_dict[file_name] = object_list

    sys.stdout.write('\r>> Converting image {:d}/{:d}'.format(num, len(file_name_list)))
    sys.stdout.flush()
    
    num += 1

sys.stdout.write('\n')

multilabels = ['aeroplane', 'bicycle', 'bird', 'boat',
               'bottle', 'bus', 'car', 'cat', 'chair',
               'cow', 'diningtable', 'dog', 'horse',
               'motorbike', 'person', 'pottedplant',
               'sheep', 'sofa', 'train', 'tvmonitor']

label_index_dict = collections.OrderedDict(zip(multilabels, 
                                               [j for j in range(20)]))

with open('classes.csv', 'w', newline='') as f:
    class_writer = csv.writer(f)

    for i in label_index_dict:
        class_writer.writerow([i, label_index_dict[i]])    

with open('annotations.csv', 'w', newline='') as f:
    anno_writer = csv.writer(f)
    
    for filename in name_object_dict:
        label_list = []
        for label in name_object_dict[filename]:
            label_list.append(label_index_dict[label])
            
#        print(filename, label_list)
        label_str = ''
        for i in set(label_list)    :
            label_str = label_str + str(i) + ' '
        
        label_str = '{}'.format(label_str.rstrip(' '))
#        print(label_str)
        anno_writer.writerow([filename, label_str])
