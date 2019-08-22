#!/usr/bin/env python3

import torch.nn as nn
from torchvision.models import vgg16
from collections import namedtuple

class Vgg16(nn.Module):
    def __init__(self):
        super(Vgg16, self).__init__()

        # the 3, 8, 15, 22th layer of features 
        # are corresponding to: relu1_2, relu2_2, relu3_3, relu4_3
        features = list(vgg16(pretrained=True).features)[:23]

        self.features = nn.ModuleList(features).eval()

    def forward(self, x):
        results = []
        for i, model in enumerate(self.features):
            x = model(x)
            
            if i in [3, 8, 15, 22]:
                results.append(x)

        vgg16_outputs = namedtuple('Vgg16Outputs', 
                                   ['relu1_2','relu2_2','relu3_3','relu4_3'])

        return vgg16_outputs(*results)



