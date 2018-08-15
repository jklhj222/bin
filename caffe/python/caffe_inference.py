#!/usr/bin/env python3
# version 1.0.1 - make functions

import os
from subprocess import call
import glob
import numpy as np
import caffe

# Assign the structure of network
MODEL_FILE = './deploy.prototxt' 
PRETRAINED = './bvlc_googlenet_iter_300000.caffemodel'

## for single picture inference
SINGLE_PRED = False
IMAGE_FILE = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/val_data/Fat_Hen/2719ff172.png'

## for multiple pictures inference
MULT_PRED = True
IMAGES_DIR = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/test/'
MEAN_FILE = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/train_data/train_mean.npy'

NUM_CLASS = 12

KAGGLE_SUBMIT = True
KAGGLE_HEADER = 'file,species'

net = caffe.Classifier(MODEL_FILE, 
                       PRETRAINED, 
                       mean=np.load(MEAN_FILE).mean(1).mean(1),
                       raw_scale=255, 
                       channel_swap=(2,1,0)
                      ) 

caffe.set_mode_gpu()
caffe.set_device(0)

## for single picture inference
def single_predict(img, num_class=NUM_CLASS):
    input_image = caffe.io.load_image(img, color=True)

#    print(input_image)
    print('prediction classes: ', num_class)
    
    prediction = net.predict([input_image], oversample = True)
    
    print('input image: ', img)
    
    for i in range(1, NUM_CLASS):
        print( 'predicted top-' + str(i) + ':', prediction[0].argsort()[-i] )
    
    print( 'prediction shape:', prediction[0].shape )
    print( 'predicted probs:', prediction[0] )

## for multiple pictures inference
def mult_predict(imgs_dir):
    imgs = [img_path for img_path in glob.glob(imgs_dir + "*")]
    
    preds = []
    for num, img in enumerate(imgs):
        input_image = caffe.io.load_image(img, color=True)
        prediction = net.predict([input_image], oversample = True)
        print(num, os.path.basename(img))
        for i in range(1,6):
            print('predicted top-' + str(i) + ':', prediction[0].argsort()[-i],
                  ',  prob = ', prediction[0][prediction[0].argsort()[-i]])
        print('')
        preds.append( prediction[0].argmax() )
    
    print(preds)
    if KAGGLE_SUBMIT:
        kaggle_submit(imgs, preds)

## make kaggle submission file
def kaggle_submit(imgs, preds):
    with open('./submission_model.csv', 'w') as f:
        f.write(KAGGLE_HEADER + '\n')
        
        for index, img in enumerate(imgs):
            f.write(os.path.basename(img) + ',' + str(preds[index]) + '\n') 

    call(["./chlabel.sh"])


if __name__ == '__main__':
    if SINGLE_PRED:
        single_predict(IMAGE_FILE)
    
    if MULT_PRED:
        mult_predict(IMAGES_DIR)
    
