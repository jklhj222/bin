#!/usr/bin/env python2
# https://blog.csdn.net/Houchaoqun_XMU/article/details/79624329
# -*- coding: utf-8 -*-
 
import pickle as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as plimg
from PIL import Image
import os
 
def load_CIFAR_batch(filename):
    """ load single batch of cifar """
    with open(filename, 'rb')as f:
#        datadict = p.load(f)
        datadict = p.load(f, encoding='latin1')
        X = datadict['data']
        Y = datadict['labels']
        X = X.reshape(10000, 3, 32, 32)
        Y = np.array(Y)
        return X, Y
 
def load_CIFAR_Labels(filename):
    with open(filename, 'rb') as f:
        lines = [x for x in f.readlines()]
        print(lines)
 
def get_class_name(lable_id):
    if(lable_id=="0"):
        class_name = "airplane"
    elif(lable_id=="1"):
        class_name = "automobile"
 
    elif(lable_id=="2"):
        class_name = "bird"
 
    elif(lable_id=="3"):
        class_name = "cat"
 
    elif(lable_id=="4"):
        class_name = "deer"
 
    elif(lable_id=="5"):
        class_name = "dog"
 
    elif(lable_id=="6"):
        class_name = "frog"
 
    elif(lable_id=="7"):
        class_name = "horse"
 
    elif(lable_id=="8"):
        class_name = "ship"
 
    elif(lable_id=="9"):
        class_name = "truck"
 
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
        imgX, imgY = load_CIFAR_batch(item)
        print("image [{}] saving...".format(item))
        xx = 0
#        for i in xrange(imgX.shape[0]):
        for i in range(imgX.shape[0]):
            imgs = imgX[i - 1]
            print("imgY = {}".format(imgY[i-1]))
            img0, img1, img2 = imgs[0], imgs[1], imgs[2]
            i0 = Image.fromarray(img0)
            i1 = Image.fromarray(img1)
            i2 = Image.fromarray(img2)
            img = Image.merge("RGB",(i0,i1,i2))
 
 
            if(folder_name == "train"):
                name = folder_name + "_" + str(train_img_num) + ".png"
            else:
                name = folder_name + "_" + str(test_img_num) + ".png"
 
            class_name = get_class_name(str(imgY[i-1]))
            save_path = os.path.join(folder_name, class_name, name)
            create_dir(os.path.join(folder_name, class_name))
            img.save(save_path, "png")
 
            train_img_num += 1
            test_img_num += 1
 
            # xx += 1
            # if(xx>10):
               #  break
 
 
if __name__ == "__main__":
    # load_CIFAR_Labels("./cifar-10-batches-py/batches.meta")
    
    binary_img_path_list = []
    binary_img_path_list.append("./cifar-10-batches-py/data_batch_1")
    binary_img_path_list.append("./cifar-10-batches-py/data_batch_2")
    binary_img_path_list.append("./cifar-10-batches-py/data_batch_3")
    binary_img_path_list.append("./cifar-10-batches-py/data_batch_4")
    binary_img_path_list.append("./cifar-10-batches-py/data_batch_5")
 
    visualize_data(binary_img_path_list, "train")
 
    test_binary_img_path_list = []
    test_binary_img_path_list.append("./cifar-10-batches-py/test_batch")
    visualize_data(test_binary_img_path_list, "validation")
