#!/usr/bin/env python3
# http://www.cnblogs.com/denny402/p/5105911.html
# 20180506, to show the parameters and weights of the caffemodel

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import caffe

MODEL = 'deploy.prototxt'
WEIGHTS = 'caffe_alexnet_train_iter_410000.caffemodel'
IMG_PATH = './7f46a71db.png'

binMeanFile = './train_mean.binaryproto'
npyMeanFile = './train_mean.npy'

caffe.set_mode_gpu()

net = caffe.Net( MODEL,
                 WEIGHTS,
                 caffe.TEST)

print('model input data shape = ', net.blobs['data'].data.shape)
print("net.blobs['data'].data.shape = ", net.blobs['data'].data.shape)

im = caffe.io.load_image(IMG_PATH)

print('input image shape = ', im.shape)

#plt.imshow(im)
#plt.axis('off')
#plt.show()


## a function to convert binary mean to python mean file
def convert_mean(binMean, npyMean):
     blob = caffe.proto.caffe_pb2.BlobProto()
     bin_mean = open(binMean, 'rb' ).read()
     blob.ParseFromString(bin_mean)
     arr = np.array( caffe.io.blobproto_to_array(blob) )
     npy_mean = arr[0]
     print(arr[0].shape)
     np.save(npyMean, npy_mean )

binMean = binMeanFile
npyMean = npyMeanFile
convert_mean(binMean,npyMean)


## load the picture into blob, and subtract the mean value
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(npyMean).mean(1).mean(1)) # subtract mean
print( 'mean value = ', np.load(npyMean).mean(1).mean(1) )
transformer.set_raw_scale('data', 255)  
transformer.set_channel_swap('data', (2,1,0))
net.blobs['data'].data[...] = transformer.preprocess('data',im)
inputData = net.blobs['data'].data
print('inputData.shape = ', inputData.shape)


## show the picture after mean subtracting
plt.figure()
plt.subplot(1,2,1),plt.title("origin")
plt.imshow(im)
plt.axis('off')
plt.subplot(1,2,2),plt.title("subtract mean")
plt.imshow( transformer.deprocess('data', inputData[0]) )
print(inputData[0].shape)
plt.axis('off')
#plt.show()

## deploy the test model, show the messages of each layer
out = net.forward()
print(len(out))
for i in out:
    print(i)
    
layer_data = [(k, v.data.shape) for k, v in net.blobs.items()]
for i in layer_data:
    print(i)

## to show the data of each layer
def show_data(data, padsize=1, padval=0):
    # normalize the data to 0-1
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    print('data shape = ', data.shape, '\n')
    n = int(np.ceil(np.sqrt(data.shape[0])))
    print('n=', n)
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) \
              + ((0, 0),) * (data.ndim - 3)
    print('padding=', padding)
    data = np.pad( data, padding, mode='constant', \
           constant_values=(padval, padval) )
    print('data.shape0: ', data.shape)

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose( (0, 2, 1, 3) 
           + tuple(range(4, data.ndim + 1)) )
    print('data.shape1: ', data.shape)
    data = data.reshape( (n * data.shape[1], n * data.shape[3]) 
           + data.shape[4:] )
    print('data.shape2: ', data.shape)

    plt.figure()
    plt.imshow(data,cmap='gray')
    plt.axis('off')
    plt.show()
    
plt.rcParams['figure.figsize'] = (8, 8)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


## display the output data and weights (filter) of first convolutional layer
print( 'output data:', net.blobs['conv1'].data.shape)
show_data(net.blobs['conv1'].data[0])
print( 'weight (filter): ', net.params['conv1'][0].data.shape )
show_data(net.params['conv1'][0].data.reshape(96*3,11,11))


## the probability of some class at last layer
feat = net.blobs['prob'].data[0]
print(net.blobs['prob'].data.shape)
print(feat)
plt.plot(feat.flat)
plt.show()

