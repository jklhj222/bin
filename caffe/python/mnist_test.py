#!/usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import caffe

caffe_root = '/home/jklhj/pkg/local/caffe'

sys.path.insert(0, caffe_root + 'python')
MODEL_FILE = './deploy.prototxt' 

PRETRAINED = '../Caffe_AlexNet_SGD_mean/caffe_alexnet_train_iter_10000.caffemodel'

IMAGE_FILE = './pngs/a006a475c.png'

input_image = caffe.io.load_image(IMAGE_FILE)

net = caffe.Classifier(MODEL_FILE, PRETRAINED)

prediction = net.predict([input_image], oversample = False)

caffe.set_mode_cpu()

print( 'predicted class: ', prediction[0].argmax() )
