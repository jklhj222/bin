#!/usr/bin/env python3

import torchvision as tv
from torchvision import transforms as T

ImageNet_mean = [0.485, 0.456, 0.406]
ImageNet_std = [0.229, 0.224, 0.225]

def get_style_data(img):
    style_transforms = T.Compose([
      T.ToTensor(),
      T.Normalize(mean=ImageNet_mean, std=ImageNet_std)
    ])

    style_img = tv.datasets.folder.default_loader(img)
    style_tensor = style_transforms(style_img)

    return style_tensor.unsqueeze(0)

# Input (b, c, h, w)
# Output (b, c, c)
def gram_matrix(y):
    (b, c, h, w) = y.size()

    features = y.view(b, c, h*w)
    
    features_t = features.transpose(1, 2)

    gram = features.bmm(features_t) / (c * h * w)

    return gram

# Input (b, c, h, w) 0~255
# Output (b, c, h, w) -2~2
def normalize_batch(batch):
    mean = batch.data.new(ImageNet_mean).view(1, -1, 1, 1)
    std = batch.data.new(ImageNet_std).view(1, -1, 1, 1)

    mean = mean.expand_as(batch.data)
    std = std.expand_as(batch.data)

    return ((batch / 255.0) - mean) / std
