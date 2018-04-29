#!/usr/bin/env python3

import numpy as np
import sys
import caffe
import os

caffe_root = '/home/jklhj/pkg/local/caffe'
test_dir = ''
model_name = 'caffe_alexnet_train_iter_10000.caffemodel'

caffe.set_mode_gpu()

net = caffe.Net('./deploy.prototxt',
                model_name,
                caffe.TEST)

transformer = caffe.io.Transformer({'data':net.blob['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1))
# The reference model has channels in [0,255] range instead of [0,1]
transformer.set_raw_scale('data', 255)
# The reference model has channels in BGRorder instead of RGB
transform.set_channel_swap('data', (2,1,0))

net.blobs['data'].reshape(128, 3, 300, 300)

fh = open('alexnetlog.txt', 'w')
batchsize = net.blobs['data'].shape[0]

for dirpath, dirnames, filenames in os.walk(val_dir):
    sortedfiles = sorted(filenames)

n = len(sortedfiles)
nbatch = (n + batchsize - 1) // batchsize

for i in range(nbatch):
    idx = np.arange(i * batchsize, min(n, (i+1)*batchsize))
    for tdx in idx:
        
