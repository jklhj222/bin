#!/usr/bin/env python3

import os
import sys
from subprocess import call
import glob
import numpy as np
import matplotlib.pyplot as plt
import caffe

# Assign the structure of network, differ with lenet_train_test.prototxt 
#MODEL_FILE = '/home/s2c/pkg/local/caffe-master_cuDNN/examples/mnist/lenet.prototxt' 
MODEL_FILE = './deploy.prototxt' 
#MODEL_FILE = 'lenet_train_test.prototxt' 
#PRETRAINED = '/home/s2c/pkg/local/caffe-master_cuDNN/examples/mnist/lenet_iter_10000.caffemodel'
PRETRAINED = './caffe_alexnet_train_iter_410000.caffemodel'

## for single picture inference
IMAGE_FILE = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/val_data/Fat_Hen/2719ff172.png'
## for multiple pictures inference
IMAGES_DIR = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/test/'

mean_file = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/train_data/train_mean.npy'

net = caffe.Classifier(MODEL_FILE, 
                       PRETRAINED, 
                       mean=np.load(mean_file).mean(1).mean(1),
                       raw_scale=255, 
                       channel_swap=(2,1,0)
                      ) 

caffe.set_mode_gpu()

## for single picture inference
#input_image = caffe.io.load_image(IMAGE_FILE, color=True)
#print(input_image)

#prediction = net.predict([input_image], oversample = True)

#print(IMAGE_FILE)

#for i in range(1,11):
#    print( 'predicted class:', i, prediction[0].argsort()[-i] )

#print( 'predicted class:', prediction[0].shape )
#print( 'predicted class:', prediction[0].argmax() )
#print( 'predicted class2:', prediction[0] )


## for multiple pictures inference
imgs = [img_path for img_path in glob.glob(IMAGES_DIR + "*.png")]

preds = []
for num, img in enumerate(imgs):
    input_image = caffe.io.load_image(img, color=True)
    prediction = net.predict([input_image], oversample = True)
    print(num, os.path.basename(img))
    for i in range(1,4):
        print('predicted class', i, prediction[0].argsort()[-i])
    preds.append( prediction[0].argmax() )

print(preds)


## make kaggle submission file
with open('./submission_model.csv', 'w') as f:
    f.write('file,species\n')
    for index, img in enumerate(imgs):
        f.write(os.path.basename(img) + ',' + str(preds[index]) + '\n') 

call(["./chlabel.sh"])
