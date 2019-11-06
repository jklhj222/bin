#!/usr/bin/env python3

import torch as t
import torchvision as tv
from torch.autograd import Variable
from PIL import Image
import torch.nn.functional as F
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import argparse

from test_dataset import TestDataset
from config import DefaultConfig as DC

parser = argparse.ArgumentParser()

parser.add_argument('--test_dir',
                    help='directory of images to test.')

parser.add_argument('--test_model',
                    help='model to be read.')

parser.add_argument('--num_class',
                    help='number of class.')

parser.add_argument('--obj_thres',
                    help='predicted object threshold',
                    default=0.9)

parser.add_argument('--seg_thres',
                    help='predicted segmentation threshold.',
                    default=0.7)

parser.add_argument('--show_img',
                    help='set to show images.',
                    action='store_true')

parser.add_argument('--save_fig',
                    help='output semantic segmentation image.',
                    default=None)

args = parser.parse_args()

test_dir = args.test_dir
test_model = args.test_model
num_class = int(args.num_class)
obj_thres = float(args.obj_thres)
seg_thres = float(args.seg_thres)
show_img = args.show_img
save_fig = args.save_fig


#test_dir = '/home/hugh/tmp/mask_rcnn_PCL_labels/images/image_resize_allRec/test'
#test_model = '/home/hugh/Dropbox/tmp-PC/model_0.pth'
#test_model = 'old_weights/model_final.pth'
#test_model = 'model_19999.pth'

test_data = TestDataset(test_dir, normalize=DC.normalize, resize=800)

test_dataloader = t.utils.data.DataLoader(test_data,
                                          batch_size=1,
                                          shuffle=False,
                                          num_workers=1)


model = tv.models.detection.__dict__['maskrcnn_resnet50_fpn'](num_classes=num_class,
                                                              pretrained=False)
model.to('cuda')

model_without_ddp = model
#model = t.nn.parallel.DistributedDataParallel(model, device_ids=0)

checkpoint = t.load(test_model, map_location='cpu')
model_without_ddp.load_state_dict(checkpoint['model'])

model_without_ddp.eval()

def save_img(img, output_file):
    img[ img>255 ] = 255

    pic_img = img.astype(np.uint8)

    Image.fromarray(pic_img).save(output_file)

for i, (data, img_path, img_width, img_height) in enumerate(test_dataloader):
    img_file = os.path.basename(img_path[0]).split('.')[0]

    print(i, img_path, img_width, img_height, img_file)

    img = Image.open(img_path[0])
    img = np.array(img, dtype='uint16') 
    print('img: ', type(img), img.shape, img.dtype)
    plt.imshow(img)
    plt.axis('off')
#    plt.show()

    with t.no_grad():
        Input = Variable(data).cuda()

        output = model(Input)

        masks = output[0]['masks'].cpu()
        print(output[0].keys())
        print('labels: ', output[0]['labels'])
        print('boxes: ', output[0]['boxes'])
        print('scores: ', output[0]['scores'])
        print('width, height: ', img_width.int(), img_height.int())

        if masks.shape[0] != 0:
            new_masks = nn.Upsample(size=(img_height.int(), img_width.int()),
                                    mode='bilinear', 
                                    align_corners=True)(masks)

            masks = masks.numpy()
            new_masks = new_masks.numpy()
#            new_masks[ new_masks > 0 ] = 255
#            np.save(str(i), new_masks)
#            with open(str(i) + '.pkl', 'wb') as f:
#                pickle.dump(new_masks, f)

        semantic = np.zeros([img_height.int(), img_width.int()])
        for i in range(new_masks.shape[0]):
#        for i in range(1):
            if output[0]['scores'][i] >= obj_thres: 
                semantic += new_masks[i, 0, ...]
#            plt.imshow(new_masks[2, 0, ...])

        print('masks.shape: ', masks.shape)
        print('new_masks.shape: ', new_masks.shape )
#        print( np.nonzero(new_masks[0, ...]) )
#        print( 'new_masks: ', new_masks[0, 0, 324, 302])
        print(np.nonzero(masks))
        print() 
        print() 

    print('np.max0: ', np.max(semantic))
    semantic[ semantic >= seg_thres ] = 120
    print('semantic: ', semantic.shape) 
    print(img[..., 1].shape)
    print('np.max1: ', np.max(semantic))
#    img[..., 1] =  2000
    print(img[..., 1].dtype, semantic.dtype) 
    print('np.max2: ', np.max(img[..., 1]))
    imgG = img[..., 1] + semantic
#    imgG[ imgG > 255 ] = 50 
    img[..., 1] = imgG

    if save_fig:
        filename = img_file + '_thres' + str(seg_thres) + '.jpg'

        save_img(img, filename)
  
    if show_img:
        plt.imshow(img)
        plt.show()


