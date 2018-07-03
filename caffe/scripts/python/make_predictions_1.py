#!/usr/bin/env python3
'''
Title           :make_predictions_1.py
Description     :This script makes predictions using the 1st trained model and generates a submission file.
Author          :Adil Moujahid
Date Created    :20160623
Date Modified   :20160625
version         :0.2
usage           :python make_predictions_1.py
#python_version  :2.7.11
python_version  :3.5.2 
'''

import os
import glob
import cv2
import caffe
import lmdb
import numpy as np
from caffe.proto import caffe_pb2
import matplotlib.pyplot as plt
from PIL import Image

latency = float( input("the latency (s) : ") )


#caffe.set_mode_gpu() 
caffe.set_mode_cpu() 

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

'''
Image processing helper function
'''

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img


'''
Reading mean image, caffe model and its weights 
'''
#Read mean image
mean_blob = caffe_pb2.BlobProto()
#with open('/home/ubuntu/deeplearning-cats-dogs-tutorial/input/mean.binaryproto') as f:
#with open('/home/s2c/pkg/local/caffe-master_cuDNN/data/ilsvrc12/imagenet_mean.binaryproto.bk', 'rb') as f:
with open('./imagenet_mean.binaryproto', 'rb') as f:
    mean_blob.ParseFromString(f.read())
mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width))

print('mean_array type = ', type(mean_array))
print('mean array shape = ', mean_array.shape)
print('mean_blob channels = ', mean_blob.channels)
print('mean_blob height = ', mean_blob.height)
print('mean_blob width = ', mean_blob.width)

#Read model architecture and trained model's weights
net = caffe.Net('./deploy.prototxt',
                './bvlc_alexnet.caffemodel',
                caffe.TEST)

#Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', mean_array)
transformer.set_transpose('data', (2,0,1))


'''
Making predicitions
'''
#Reading image paths
test_img_paths = [img_path for img_path in glob.glob("./ILSVRC2012_img_test/*.JPEG")]

#Making predictions
with open("./test_ground_truth_dict.txt") as test_label :
    test_label_dict = eval(test_label.read())
    
with open("./imagenet1000_clsid_to_human.txt") as ID_lebel :
    ID_label_dict = eval(ID_lebel.read())

test_ids = []
preds = []
ims = []

fig = plt.figure()
plt.ion()

for img_path in test_img_paths:
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
    img_filename = os.path.basename(img_path)
    
    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    out = net.forward()
    pred_probas = out['prob']

    test_ids = test_ids + [img_path.split('/')[-1][:-4]]
    preds = preds + [pred_probas.argmax()]

    ID_ground_truth = test_label_dict[img_filename]

    print(img_path, "\n")
    print(pred_probas.argmax(), ID_label_dict[pred_probas.argmax()])

    top5_label = []
    for i in range(1,6):
        if ID_label_dict[ID_ground_truth] == ID_label_dict[pred_probas.argsort(1)[1,-i]] :
            print("{:d}.".format(i), pred_probas.argsort(1)[1,-i], 
                  ID_label_dict[pred_probas.argsort(1)[1,-i]], "      <---------------------------")
        else:
            print("{:d}.".format(i), pred_probas.argsort(1)[1,-i], 
                  ID_label_dict[pred_probas.argsort(1)[1,-i]])
     
        top5_label.append(ID_label_dict[pred_probas.argsort(1)[1,-i]])

    print("\nGround truth : ", ID_label_dict[ID_ground_truth])


    plt.clf()
    plot1 = fig.add_subplot(211)
    plt.subplots_adjust(left=0.0, bottom=0.0, top=0.80, right=1.0)

    imr = plt.imread(img_path)
    ratio = imr.shape[0]/100

    plot1.title.set_position([0.5, 1.1])
    plot1.set_title("{:>20s}".format('Gound Truth : ') + ID_label_dict[ID_ground_truth] + 
                    "{:>20s}".format('\nTop-1 Prediction : ') + 
                    ID_label_dict[pred_probas.argsort(1)[1,-1]], loc='center', fontsize=18)

    plt.text(0, imr.shape[0]+ratio*20 , 'Top-5 Prediction :', fontsize=18)

    for i in range(0,5) :
        if ID_label_dict[ID_ground_truth] == ID_label_dict[pred_probas.argsort(1)[1,-(i+1)]] :
            plt.text(0, imr.shape[0]+ratio*33 + ratio*10*i, str(i+1) + ". " + top5_label[i] 
                     , color='red', fontsize=15)
        else :
            plt.text(0, imr.shape[0]+ratio*33 + ratio*10*i, str(i+1) + ". " + top5_label[i]
                     , fontsize=15)
    
    print('-------')

    plt.imshow(imr)
    plt.show()
    plt.pause(latency)

'''
Making submission file
'''
with open("./submission_model_1.csv","w") as f:
    f.write("id,label\n")
    for i in range(len(test_ids)):
        f.write(str(test_ids[i])+","+str(preds[i])+"\n")
f.close()
