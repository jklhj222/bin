#!/usr/bin/env python3
""" Created on Thu Oct 11 16:24:29 2018 @author: jklhj """

import csv
import random

train_set_percentage = 0.8

with open('train_orig.csv', newline='') as f:
    rows = list(csv.reader(f))[1:]
    
    for i, row in enumerate(rows):
        print(i, row)
        
    print('total rows: ', i+1)
    
    total_idx = [idx for idx in range(i+1)]
    
    train_set_idx = sorted(random.sample(total_idx, 
                                         int(i*train_set_percentage)))
    
    val_set_idx = list(set(total_idx) - set(train_set_idx))
    
    train_set = []
    for i in train_set_idx:
        train_set.append(rows[i])
        
    val_set = []
    for i in val_set_idx:
        val_set.append(rows[i])
        
with open('train.csv', 'w', newline='') as f:
    train_writer = csv.writer(f)
    
    train_writer.writerows(train_set)
    
with open('val.csv', 'w', newline='') as f:
    val_writer = csv.writer(f)
    
    val_writer.writerows(val_set)
