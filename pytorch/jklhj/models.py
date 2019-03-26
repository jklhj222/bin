#!/usr/bin/env python3
import torchvision as tv

class ResNet50(tv.models.resnet50):
    def __init__(self, input_size, avgpool_kernel_size):
        super(ResNet50, self).__init__()
   
