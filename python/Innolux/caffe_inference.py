#!/usr/bin/env python3
# version 1.0.1 - make functions

import os
from subprocess import call
import glob
import numpy as np
import caffe
import time
import shutil
from PIL import Image
from PIL import ImageDraw
from math import floor

init_t = time.time()

TEST = 'test hello world'

#val_set = {'before':('before',0), 'middle':('middle',1), 'after':('after',2)}
val_set_string = 'after'
val_set = {'before' : 0, 'middle' : 1, 'after' : 2}

SINGLE_PRED = False
MULT_PRED = True 

KAGGLE_SUBMIT = False
KAGGLE_HEADER = 'file,species'

# Assign the structure of network
MODEL_FILE = './ResNet-50-deploy.prototxt' 
PRETRAINED = './resnet_50_iter_200000.caffemodel'

## for single picture inference
IMAGE_FILE = '/mnt/sda1/work/Innolux/ML_RawData/3_Train/120h.120w_size_train_val/data_before/train/7570F376D0T5PC05011_120x.120y.JPG'

## for multiple pictures inference
IMAGES_DIR = '/mnt/sda1/work/Innolux/ML_RawData/3_Train/100h.100w_size_train_val/data_' + val_set_string + '/cut_size/val/'

ORIGIN_DIR = '/mnt/sda1/work/Innolux/ML_RawData/3_Train/100h.100w_size_train_val/data_' + val_set_string + '/origin_size/val/'

MEAN_FILE = '/mnt/sda1/work/Innolux/ML_RawData/3_Train/100h.100w_size_train_val/train_mean.npy'

NUM_CLASS = 3

net = caffe.Classifier(MODEL_FILE, 
                       PRETRAINED, 
                       mean=np.load(MEAN_FILE).mean(1).mean(1),
                       raw_scale=255, 
                       channel_swap=(2,1,0)
                      ) 

caffe.set_mode_gpu()

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

    if os.path.exists('./prediction/' + val_set_string):
        shutil.rmtree('./prediction/' + val_set_string)
    if not os.path.exists('./prediction/' + val_set_string):
        os.makedirs('./prediction/' + val_set_string)

    os.makedirs('./prediction/' + val_set_string + '/0')
    os.makedirs('./prediction/' + val_set_string + '/1')
    os.makedirs('./prediction/' + val_set_string + '/2')

    j, k = 0, 0

    for num, img in enumerate(imgs):
        input_image = caffe.io.load_image(img, color=True)
        prediction = net.predict([input_image], oversample = True)
        print(num, os.path.basename(img))
        print(num, img)
        origin_filename = os.path.basename(img).split('_')[0] + '.JPG'

        cut_size_xy = ( int(os.path.basename(img).split('.')[-3][-4:-1]), int(os.path.basename(img).split('.')[-2][0:3]) )
        print(cut_size_xy)

        for i in range(1,2):
            print('predicted top-' + str(i) + ':', prediction[0].argsort()[-i])

            if prediction[0].argsort()[-i] == val_set[val_set_string]: 
                print('-----------------------------------------------------'\
                      '-------------------------------')

            image = Image.open(ORIGIN_DIR + origin_filename)

            image_frame = ImageDraw.Draw(image) 

            if image.size == (640, 480):
                x = floor( (image.size[0] - cut_size_xy[0])/2 )
                y = floor( (image.size[1] - cut_size_xy[1])/2 )
                xw = x + cut_size_xy[0]
                yh = y + cut_size_xy[1]

            else:
                x = floor( (image.size[0] - cut_size_xy[0])/2 ) 
                y = floor( (image.size[1] - cut_size_xy[1])/2 ) - 42 
                xw = x + cut_size_xy[0]
                yh = y + cut_size_xy[1]

            image_frame.line( ((x, y), (x, yh)),  (255, 0, 0), width=5 )
            image_frame.line( ((x, y), (xw, y)),  (255, 0, 0), width=5 )
            image_frame.line( ((x, yh), (xw, yh)),  (255, 0, 0), width=5 )
            image_frame.line( ((xw, y), (xw, yh)),  (255, 0, 0), width=5 )

#            image_frame.line( ((280, 180), (280, 300)), (255, 0, 0), width=5 )
#            image_frame.line( ((280, 180), (400, 180)), (255, 0, 0), width=5 )
#            image_frame.line( ((280, 300), (400, 300)), (255, 0, 0), width=5 )
#            image_frame.line( ((400, 180), (400, 300)), (255, 0, 0), width=5 )

            image.save('./prediction/' + val_set_string + '/' +
                       str(prediction[0].argsort()[-i]) + 
                       '/' + origin_filename)

#            shutil.copy( ORIGIN_DIR + origin_filename, './prediction/after/'\
#                           + str(prediction[0].argsort()[-i]) )

        print('')
        preds.append( prediction[0].argmax() )
        if prediction[0].argsort()[-i] == val_set[val_set_string]: j += 1
    print(preds)
    print('total numver : ', len(preds), 'correct number : ', j, 'accuracy : ', j/len(preds))

if __name__ == '__main__':
    if SINGLE_PRED:
        single_predict(IMAGE_FILE)

    if MULT_PRED:
        mult_predict(IMAGES_DIR)

final_t = time.time()
print('time = ', final_t - init_t)




