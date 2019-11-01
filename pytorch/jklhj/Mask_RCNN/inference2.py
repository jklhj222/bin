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

from test_dataset import TestDataset
from config import DefaultConfig as DC

#test_dir = '/home/hugh/tmp/coco_test/val2017_short'
test_dir = '/home/hugh/tmp/mask_rcnn_PCL_labels/images/image_resize/test'
#test_model = '/home/hugh/Dropbox/tmp-PC/model_0.pth'
#test_model = 'old_weights/model_final.pth'
test_model = 'model_18000.pth'

test_data = TestDataset(test_dir, normalize=DC.normalize, resize=800)

test_dataloader = t.utils.data.DataLoader(test_data,
                                          batch_size=1,
                                          shuffle=False,
                                          num_workers=2)


#model = tv.models.detection.__dict__['maskrcnn_resnet50_fpn'](num_classes=2,
#                                                              pretrained=False)
model = tv.models.detection.__dict__['maskrcnn_resnet50_fpn'](num_classes=2,
                                                                 pretrained=False)
model.to('cuda')

model_without_ddp = model
#model = t.nn.parallel.DistributedDataParallel(model, device_ids=0)

#print(model)

checkpoint = t.load(test_model, map_location='cpu')
model_without_ddp.load_state_dict(checkpoint['model'])

model_without_ddp.eval()

#print(model_without_ddp)

for i, (data, img_path, img_width, img_height) in enumerate(test_dataloader):
    print(i, img_path, img_width, img_height)

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
            if output[0]['scores'][i]>0.9: semantic += new_masks[i, 0, ...]
#            plt.imshow(new_masks[2, 0, ...])

        print('masks.shape: ', masks.shape)
        print('new_masks.shape: ', new_masks.shape )
#        print( np.nonzero(new_masks[0, ...]) )
#        print( 'new_masks: ', new_masks[0, 0, 324, 302])
        print(np.nonzero(masks))
        print() 
        print() 

    print('np.max0: ', np.max(semantic))
    semantic[ semantic > 0 ] = 80
    print('semantic: ', semantic.shape) 
    print(img[..., 1].shape)
    print('np.max1: ', np.max(semantic))
#    img[..., 1] =  2000
    print(img[..., 1].dtype, semantic.dtype) 
    print('np.max2: ', np.max(img[..., 1]))
    imgG = img[..., 1] + semantic
#    imgG[ imgG > 255 ] = 50 
    img[..., 1] = imgG

    plt.imshow(img)
    plt.show()


