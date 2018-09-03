#!/usr/bin/env python2
""" Created on Wed Aug 29 16:05:01 2018 @author: jklhj """

import argparse
import cv2
from math import floor

parser = argparse.ArgumentParser(
        description='For Caffe ssd image detection (use python2), '
                     'and return the coordinates of bounding box.')

parser.add_argument('--root_caffe_ssd',
                    default='',
                    help='Caffe pycaffe directory (python2).')

parser.add_argument('--set_gpu',
                    help='set to use GPU.',
                    default=False,
                    action='store_true')
parser.add_argument('--gpu_index',
                    help='the index of GPU.',
                    default=None)

parser.add_argument('--deploy_model',
                    default='',
                    help='the prototxt file of deployment.')

parser.add_argument('--pretrain_model',
                    default='',
                    help='the pretrain model (*.caffemodel) of deployment.')

parser.add_argument('--image_file',
                    default='',
                    help='the image file to detect.')

args = parser.parse_args()

if not args.root_caffe_ssd: print('Error: Need to set the caffe ssd root: '
                                  '--root_caffe_ssd')
if not args.deploy_model: print('Error: Need to set deploy prototxt file: '
                                '--deploy_model')
if not args.pretrain_model: print('Error: Need to set pretrained model: '
                                  '--pretrain_model')
if not args.image_file: print('Error: Need to set image file to detect: '
                              '--image_file')

img = cv2.imread(args.image_file)
height, width, channels = img.shape 

import sys
sys.path.insert(0, args.root_caffe_ssd)

import caffe

if args.set_gpu:
    caffe.set_device(int(args.gpu_index))
    caffe.set_mode_gpu()


def caffe_ssd_img_detection(deploy_model,
                            pretrain_model,
                            image_file):
    
    net = caffe.Net(deploy_model,
                    pretrain_model,
                    caffe.TEST)
    
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
#    transformer.set_mean('data', np.array([104,117,123])) # mean pixel
    
    ## the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_raw_scale('data', 255) 
    ## the reference model has channels in BGR order instead of RGB
    transformer.set_channel_swap('data', (2,1,0)) 
    
    image = caffe.io.load_image(image_file)
    
    transformed_image = transformer.preprocess('data', image)
    
    net.blobs['data'].data[0,...] = transformed_image
 
    detections = net.forward()['detection_out']
    
    det_label = detections[0,0,:,1]
    det_conf  = detections[0,0,:,2]
    det_xmin  = detections[0,0,:,3]
    det_ymin  = detections[0,0,:,4]
    det_xmax  = detections[0,0,:,5]
    det_ymax  = detections[0,0,:,6]

    return det_label, det_conf, det_xmin, det_ymin, det_xmax, det_ymax
    
if __name__ == '__main__':
    
    label, conf, xmin, ymin, xmax, ymax = \
      caffe_ssd_img_detection(args.deploy_model,
                              args.pretrain_model,
                              args.image_file)
    label = list(label)
    conf = list(conf) 
    xmin = list(xmin*width)
    xmax = list(xmax*width)
    ymin = list(ymin*height)
    ymax = list(ymax*height)   


    print('label: ', list(label))
    print('conf: ', list(conf))
    print('xmin: ', map( int, xmin ))
    print('xmax: ', map( int, xmax ))
    print('ymin: ', map( int, ymin ))
    print('ymax: ', map( int, ymax ))
    print('imgag height, width, channels: ', height, width, channels)
   
    cv2.rectangle( img, (xmin[0], ymin[0]), (xmax[0], ymax[0]), (0, 0, 255), 5 ) 
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText( img, str(label[0]), (xmin[0], ymin[0]), font, 0.7, (255, 255, 255), 1 )
    cv2.imshow('test', img)
    cv2.waitKey(0)
