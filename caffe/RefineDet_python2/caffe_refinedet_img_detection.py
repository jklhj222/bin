#!/usr/bin/env python2
""" Created on Wed Aug 29 16:05:01 2018 @author: jklhj """

import argparse
import cv2
import os
import shutil

parser = argparse.ArgumentParser(
        description='For Caffe ssd image detection (use python2), '
                    'and return the coordinates of the bounding boxes.')

parser.add_argument('--root_caffe_ssd',
                    default='',
                    help='Caffe ssd pycaffe directory (python2).')

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

parser.add_argument('--labelmap_file',
                    default='',
                    help='the label map file.')

parser.add_argument('--conf_threshold',
                    default=0.5,
                    help='the confidence threshold in ssd detection, default=0.5 .')

parser.add_argument('--image_file',
                    default='',
                    help='the image file to detect.')

parser.add_argument('--show_img',
                    help='set to show the image with bounding boxes.',
                    default=False,
                    action='store_true')

args = parser.parse_args()

if (args.set_gpu) and (not args.gpu_index): print('Error: Need to set the index of GPU: '
                                                  '--gpu_index')

if not args.root_caffe_ssd: print('Error: Need to set the caffe ssd root: '
                                  '--root_caffe_ssd')
if not args.deploy_model: print('Error: Need to set deploy prototxt file: '
                                '--deploy_model')
if not args.pretrain_model: print('Error: Need to set pretrained model: '
                                  '--pretrain_model')
if not args.labelmap_file: print('Error: Need to set label map file: '
                                  '--label_map_file')
if not args.image_file: print('Error: Need to set image file to detect: '
                              '--image_file')

img = cv2.imread(args.image_file)
height, width, channels = img.shape 

import sys
sys.path.insert(0, args.root_caffe_ssd)

import caffe
from caffe.proto import caffe_pb2
from google.protobuf import text_format

if args.set_gpu:
    caffe.set_device(int(args.gpu_index))
    caffe.set_mode_gpu()

def get_modify_output_layer_param(conf_threshold, deploy_model):
    net = caffe_pb2.NetParameter()

    with open(deploy_model, 'r') as f:
        text_format.Merge(f.read(), net)
    
    layerName = [ l.name for l in net.layer ]
    idx = layerName.index('detection_out')
    
    output_layer = net.layer[idx]
    
    # modify output parameter
    output_layer.detection_output_param.confidence_threshold = float(conf_threshold)
    
    # get output parameter
#    LabelMapFile = output_layer.detection_output_param.save_output_param.label_map_file

    shutil.copyfile(deploy_model, deploy_model + '_orig')
    os.remove(deploy_model)

    with open(deploy_model, 'w') as f:
        f.write(str(net))    

#    return LabelMapFile, conf_threshold
    return conf_threshold

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

def show_image(img, xmin, xmax, ymin, ymax, label_names):
    for i in range(len(xmin)):
        cv2.rectangle( img, (xmin[i], ymin[i]), (xmax[i], ymax[i]), (0, 0, 255), 3 ) 
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText( img, str(label_names[i]), 
                     (xmin[i], ymin[i]), font, 0.7, (255, 255, 255), 1 )
        cv2.putText( img, '{:.2f}'.format(conf[i]), 
                     (xmin[i], ymin[i]-20), font, 0.7, (255, 255, 255), 1 )

    cv2.imshow('Image', img)
    cv2.waitKey(0)

if __name__ == '__main__':

    conf_thres = \
      get_modify_output_layer_param(args.conf_threshold, args.deploy_model)
    
    label, conf, xmin, ymin, xmax, ymax = \
      caffe_ssd_img_detection(args.deploy_model,
                              args.pretrain_model,
                              args.image_file)
    label = list(label)
    conf = list(conf) 
    xmin = map( int, list(xmin*width) )
    xmax = map( int, list(xmax*width) )
    ymin = map( int, list(ymin*height) )
    ymax = map( int, list(ymax*height) )

    # get label names
    label_names = []
    with open(args.labelmap_file, 'r') as f:
        labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(f.read()), labelmap)
        for i in label:
            label_names.append( str(labelmap.item[int(i)].display_name) )

    print('conf threshold: ', conf_thres)
    print('label: ', list(label))
    print('label name:', label_names)
    print('conf: ', list(conf))
    print('xmin: ', map( int, xmin ))
    print('xmax: ', map( int, xmax ))
    print('ymin: ', map( int, ymin ))
    print('ymax: ', map( int, ymax ))
    print('image height, width, channels: ', height, width, channels)

    if args.show_img:
        show_image(img, xmin, xmax, ymin, ymax, label_names)

