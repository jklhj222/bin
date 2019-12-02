#!/usr/bin/env python3
""" Created on Tue Mar 26 10:14:20 2019 @author: jklhj """

import os
import cv2
import numpy as np

def GetFileList(path):
    root, dirs, files = next(os.walk(path))

    file_list = []

    for dirr in dirs:
        content = os.listdir(os.path.join(root, dirr))
        print(content)
        file = [os.path.join(root, dirr, i) for i in content]
        print(file)
        file_list.extend(file)

    return file_list

def ComputeMean(file_list, grayscale=False):
    
    if grayscale:
        per_image_Graymean = []

    else:
        per_image_Rmean = []
        per_image_Gmean = []
        per_image_Bmean = []

    for file_name in file_list:
        if grayscale:
            img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            
            per_image_Graymean.append(np.mean(img))

        else:
            img = cv2.imread(file_name, 1)
            (B, G, R) = cv2.split(img)
        
            per_image_Bmean.append(np.mean(B))
            per_image_Gmean.append(np.mean(G))
            per_image_Rmean.append(np.mean(R))

    if grayscale:
        Gray_mean = np.mean(per_image_Graymean)

        return Gray_mean

    else:
        R_mean = np.mean(per_image_Rmean)
        G_mean = np.mean(per_image_Gmean)
        B_mean = np.mean(per_image_Bmean)

        return R_mean, G_mean, B_mean


def ComputeSTD(file_list, GrayRGB_mean, grayscale=False):
    if grayscale:
        Gray_mean = GrayRGB_mean

        per_image_Graysum_sqrErr = []

    else:
        B_mean = GrayRGB_mean[2]
        G_mean = GrayRGB_mean[1]
        R_mean = GrayRGB_mean[0]
    
        per_image_Rsum_sqrErr = []
        per_image_Gsum_sqrErr = []
        per_image_Bsum_sqrErr = []

    for file_name in file_list:
        if grayscale:
            img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

            per_image_Graysum_sqrErr.append( np.square(img-GrayRGB_mean).mean() )

        else:
            img = cv2.imread(file_name, 1)
            (B, G, R) = cv2.split(img)
        
            per_image_Bsum_sqrErr.append( np.square(B-B_mean).mean() ) 
            per_image_Gsum_sqrErr.append( np.square(G-G_mean).mean() )
            per_image_Rsum_sqrErr.append( np.square(R-R_mean).mean() )

    if grayscale:
        Gray_std = np.sqrt( np.mean(per_image_Graysum_sqrErr) )
 
        return Gray_std

    else:
        R_std = np.sqrt( np.mean(per_image_Rsum_sqrErr) )
        G_std = np.sqrt( np.mean(per_image_Gsum_sqrErr) )
        B_std = np.sqrt( np.mean(per_image_Bsum_sqrErr) )
    
        return R_std, G_std, B_std

 
if __name__ == '__main__':
    path = './train_data/'
    grayscale = True 

    file_list = GetFileList(path)
    print('\n# files: ', len(file_list))

    if grayscale:
        Gray_mean = ComputeMean(file_list, grayscale=True)
        print('Gray mean: ', Gray_mean)
        print('Gray mean: ', Gray_mean/255, '\n')

        Gray_std = ComputeSTD(file_list, Gray_mean, grayscale=True)
        print('Gray std: ', Gray_std)
        print('Gray std: ', Gray_std/255)

    else:
        R_mean, G_mean, B_mean = ComputeMean(file_list)
        print('RGB mean: ', R_mean, ',', G_mean, ',', B_mean)
        print('RGB mean: ', R_mean/255, ',', G_mean/255, ',', B_mean/255, '\n')

        R_std, G_std, B_std = ComputeSTD(file_list, (R_mean, G_mean, B_mean))
        print('RGB std: ', R_std, ',', G_std, ',', B_std)
        print('RGB std: ', R_std/255, ',', G_std/255, ',', B_std/255)




