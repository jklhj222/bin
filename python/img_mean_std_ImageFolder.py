#!/usr/bin/env python3
""" Created on Tue Mar 26 10:14:20 2019 @author: jklhj """

import os
import cv2
import numpy as np

path = '/home/hugh/Dropbox/tmp-PC/pytorch/train_all'

root, dirs, files = next(os.walk(path))

file_list = []

for dirr in dirs:
    content = os.listdir(os.path.join(root, dirr))
    print(content)
    file = [os.path.join(root, dirr, i) for i in content]
    print(file)
    file_list.extend(file)


def compute_mean(file_list):
    
    per_image_Rmean = []
    per_image_Gmean = []
    per_image_Bmean = []

    for file_name in file_list:
        img = cv2.imread(file_name, 1)
        (B, G, R) = cv2.split(img)
        
        per_image_Bmean.append(np.mean(B))
        per_image_Gmean.append(np.mean(G))
        per_image_Rmean.append(np.mean(R))

    R_mean = np.mean(per_image_Rmean)
    G_mean = np.mean(per_image_Gmean)
    B_mean = np.mean(per_image_Bmean)

    return R_mean, G_mean, B_mean


def compute_std(file_list, RGB_mean):

    B_mean = RGB_mean[2]
    G_mean = RGB_mean[1]
    R_mean = RGB_mean[0]
    
    per_image_Rsum_sqrErr = []
    per_image_Gsum_sqrErr = []
    per_image_Bsum_sqrErr = []

    for file_name in file_list:
        img = cv2.imread(file_name, 1)
        (B, G, R) = cv2.split(img)
        
        per_image_Bsum_sqrErr.append( np.square(B-B_mean).mean() ) 
        per_image_Gsum_sqrErr.append( np.square(G-G_mean).mean() )
        per_image_Rsum_sqrErr.append( np.square(R-R_mean).mean() )

    R_std = np.sqrt( np.mean(per_image_Rsum_sqrErr) )
    G_std = np.sqrt( np.mean(per_image_Gsum_sqrErr) )
    B_std = np.sqrt( np.mean(per_image_Bsum_sqrErr) )
    
    return R_std, G_std, B_std

 
if __name__ == '__main__':
    R_mean, G_mean, B_mean = compute_mean(file_list)
    print('RGB mean: ', R_mean, G_mean, B_mean)

    R_std, G_std, B_std = compute_std(file_list, (R_mean, G_mean, B_mean))
    print('RGB std: ', R_std, G_std, B_std)




