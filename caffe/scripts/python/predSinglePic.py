#!/usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import caffe

caffe_root = '/home/jklhj/pkg/local/caffe'

sys.path.insert(0, caffe_root + 'python')
MODEL_FILE = './lenet.prototxt' 

PRETRAINED = './lenet_iter_10000.caffemodel'

IMAGE_FILE = './4.png'

input_image = caffe.io.load_image(IMAGE_FILE, color=False)

net = caffe.Classifier(MODEL_FILE, PRETRAINED)

prediction = net.predict([input_image], oversample = False)

caffe.set_mode_cpu()

print( 'predicted class: ', prediction[0].argmax() )
print( 'predicted class all: ', prediction[0] )
