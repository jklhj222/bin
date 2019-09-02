#!/usr/bin/env python3

from torchsummary import summary
from torchvision.models import resnet152
from torchvision.models import vgg16 
from torchvision.models import alexnet 

#model = resnet152().cuda()
#model = vgg16().cuda()
model = alexnet().cuda()

print(summary(model, (3, 324, 324), device='cuda'))
#print('model.fc.in_features: ', model.fc.in_features)
#print('model.fc: ', model.fc)

