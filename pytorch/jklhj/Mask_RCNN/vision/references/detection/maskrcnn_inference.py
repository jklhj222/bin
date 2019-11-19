#!/usr/bin/env python3

import torch as t
import torchvision as tv 
from torchvision import transforms as T

def maskrcnn_inference(img, 
                       premodel, 
                       num_classes,
                       model='maskrcnn_resnet50_fpn'):

    num_classes += 1

    model = tv.models.detection.__dict__[model](num_classes=num_classes,
                                                pretrained=False)

    model.to('cuda')

    checkpoint = t.load(premodel, map_location='cpu')

    model.load_state_dict(checkpoint['model'])
    
    model.eval()

    height, width, ch = img.shape

    transforms = T.Compose([
      T.ToPILImage(),
      T.Resize((800, 800)), 
      T.ToTensor()
      ])
 
    data = transforms(img)

    data = data.unsqueeze(0)

    with t.no_grad():
        Input = t.autograd.Variable(data).cuda()

        output = model(Input)

        masks = output[0]['masks'].cpu()

        new_masks = t.nn.Upsample(size=(height, width),
                                  mode='bilinear',
                                  align_corners=True)(masks)

        new_masks = new_masks.numpy()

        top1_instance = new_masks[0, ...]

        return top1_instance


if __name__ == '__main__':
    import cv2
    import matplotlib.pyplot as plt
    import numpy as np

    premodel = 'model_100.pth'
    num_class = 1
    img = cv2.imread('/home/hugh/tmp/mask_rcnn_PCL_labels/images/images_origin/Fside_C1_0001_244d46X_50Y_72d03Z-CCD1_004.jpg')

    masks = maskrcnn_inference(img, premodel, num_class)
    masks[masks > 0.8] = 200 

    print(masks, type(masks), masks.shape, np.max(masks))
    plt.imshow(masks.squeeze())
    plt.show()

