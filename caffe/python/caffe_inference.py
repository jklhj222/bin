#!/usr/bin/env python3
# version 1.1.0 - argumentize

import os
import argparse
import numpy as np
import glob
import caffe

parser = argparse.ArgumentParser(
        description='For Caffe inference of classification.')

parser.add_argument('--root_caffe',
                    default='',
                    help='Caffe root directory.')

parser.add_argument('--set_gpu',
                    help='set to use GPU.',
                    default=False,
                    action='store_true')

parser.add_argument('--gpu_index',
                    help='the index of GPU.',
                    default=0)

parser.add_argument('--deploy_model',
                    default='',
                    help='the prototxt file of deployment.')

parser.add_argument('--pretrain_model',
                    default='',
                    help='the pretrain model (*.caffemodel) of deployment.')

parser.add_argument('--mean_file',
                    default='',
                    help='the mean value file of the pretrained model.')

parser.add_argument('--image_file',
                    default='',
                    help='the image file to detect.')

parser.add_argument('--images_dir',
                    default='',
                    help='the directory of image files (for multiple detection).')

parser.add_argument('--top_predict',
                    default=None,
                    help='the top number of class to predict.')

args = parser.parse_args()

if args.set_gpu and not args.gpu_index: print('Error: Need to set the '
                                                  'index of GPU: '
                                                  '--gpu_index')

if not args.root_caffe: print('Error: Need to set the caffe ssd root: '
                                  '--root_caffe')
if not args.deploy_model: print('Error: Need to set deploy prototxt file: '
                                '--deploy_model')
if not args.pretrain_model: print('Error: Need to set pretrained model: '
                                  '--pretrain_model')
if not args.mean_file: print('Error: Need to set mean value file: '
                                  '--mean_file')
if not args.image_file and not args.images_dir: print('Error: Need to set '
                                                      'image file or directory'
                                                      ' of images to detect: '
                                                      '--image_file or '
                                                      '--images_dir')

if args.set_gpu:
    caffe.set_device(int(args.gpu_index))
    caffe.set_mode_gpu()

import sys
sys.path.insert(0, args.root_caffe + '/python/')

#KAGGLE_SUBMIT = True
#KAGGLE_HEADER = 'file,species'

net = caffe.Classifier(args.deploy_model, 
                       args.pretrain_model, 
                       mean=np.load(args.mean_file).mean(1).mean(1),
                       raw_scale=255, 
                       channel_swap=(2,1,0)
                      ) 


## for single picture inference
def single_predict(img, top_predict=args.top_predict):
    input_image = caffe.io.load_image(img, color=True)

#    print(input_image)
    print('Top-' + str(top_predict), 'predict')
    
    prediction = net.predict([input_image], oversample = True)
    
    print('input image: ', img)
    
    for i in range(1, int(top_predict)+1):
        print( 'predicted top-' + str(i) + ':', prediction[0].argsort()[-i] )
    
    print( 'prediction shape:', prediction[0].shape )
    print( 'predicted probs:', prediction[0] )

## for multiple pictures inference
def mult_predict(imgs_dir, top_predict=args.top_predict):
    imgs = [img_path for img_path in glob.glob(imgs_dir + "*")]
    preds = []
    for num, img in enumerate(imgs):
        input_image = caffe.io.load_image(img, color=True)
        prediction = net.predict([input_image], oversample = True)
        print(num, os.path.basename(img))
        for i in range(1, int(top_predict)+1):
            print('predicted top-' + str(i) + ':', prediction[0].argsort()[-i],
                  ',  prob = ', prediction[0][prediction[0].argsort()[-i]])
        print('')
        preds.append( prediction[0].argmax() )
    
    return preds
#    if KAGGLE_SUBMIT:
#        kaggle_submit(imgs, preds)
#
## make kaggle submission file
#def kaggle_submit(imgs, preds):
#    with open('./submission_model.csv', 'w') as f:
#        f.write(KAGGLE_HEADER + '\n')
#        
#        for index, img in enumerate(imgs):
#            f.write(os.path.basename(img) + ',' + str(preds[index]) + '\n') 
#
#    call(["./chlabel.sh"])

if __name__ == '__main__':
    if args.image_file:
        single_predict(args.image_file)
    
    if args.images_dir:
        mult_predict(args.images_dir + '/')
    
