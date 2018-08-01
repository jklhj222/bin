#!/usr/bin/env python3
# https://blog.csdn.net/Houchaoqun_XMU/article/details/79624329
# -*- coding: utf-8 -*-
 
import pickle as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as plimg
from PIL import Image
import os
 
def load_CIFAR_batch(filename, folder_name):
    """ load single batch of cifar """
    with open(filename, 'rb')as f:
        datadict = p.load(f)
        """ 
        cifar100 data content: 
            { 
            "coarse_labels":[0,...,19],   # 0~19 super category 
            "filenames":["volcano_s_000012.png",...], 
            "batch_label":"", 
            "fine_labels":[0,1...99]      # 0~99 category 
            } 
        return list of numpy arrays [na,...,na] with specific batch_size 
                na: N dimensional numpy array  
        """  
        # print(datadict.keys())
        ## ['data', 'batch_label', 'fine_labels', 'coarse_labels', 'filenames']
 
        batch_label = datadict['batch_label']
        fine_labels = datadict['fine_labels']
        coarse_labels = datadict['coarse_labels']
        batch_label = np.array(batch_label)
        fine_labels = np.array(fine_labels)
        coarse_labels = np.array(coarse_labels)
 
        X = datadict['data']
        # print(X.shape)
        if(folder_name == "train"):
            X = X.reshape(50000, 3, 32, 32)
        elif(folder_name == "validation"):
            X = X.reshape(10000, 3, 32, 32)
 
        return X, batch_label, fine_labels, coarse_labels
 
def unpickle(file):  
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict
 
 
filename = "./cifar-100-python/meta"
dict_meta_batch = unpickle(filename)
 
def get_class_name(lable_id):
    
    fine_label_names_list = dict_meta_batch['fine_label_names']
    class_name = fine_label_names_list[lable_id]
 
    return class_name
 
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        print("Create dir = {}".format(dir_path))
        os.makedirs(dir_path)
 
train_img_num = 0
test_img_num = 0
def visualize_data(binary_img_path_list, folder_name):
    global train_img_num
    global test_img_num
    for item in binary_img_path_list:
        # imgX, imgY = load_CIFAR_batch(item)
        imgX, batch_label, fine_labels, coarse_labels = load_CIFAR_batch(item, folder_name)
        print("image [{}] saving...".format(item))
        xx = 0
        for i in xrange(imgX.shape[0]):
            imgs = imgX[i - 1]
            # print("fine_labels = {}".format(fine_labels[i-1]))
            img0, img1, img2 = imgs[0], imgs[1], imgs[2]
            i0 = Image.fromarray(img0)
            i1 = Image.fromarray(img1)
            i2 = Image.fromarray(img2)
            img = Image.merge("RGB",(i0,i1,i2))
 
            class_name = get_class_name(fine_labels[i-1])
            print("class_name = {}".format(class_name))
 
            if(folder_name == "train"):
                name = class_name + "_" + str(train_img_num) + ".png"
            else:
                name = class_name + "_" + str(test_img_num) + ".png"
 
            save_path = os.path.join(folder_name, class_name, name)
            create_dir(os.path.join(folder_name, class_name))
            img.save(save_path, "png")
 
            train_img_num += 1
            test_img_num += 1
 
            # xx += 1
            # if(xx>10):
            #     break
 
 
if __name__ == "__main__":
    
    binary_img_path_list = []
    binary_img_path_list.append("./cifar-100-python/train")
    visualize_data(binary_img_path_list, "train")
 
    test_binary_img_path_list = []
    test_binary_img_path_list.append("./cifar-100-python/test")
    visualize_data(test_binary_img_path_list, "validation")
