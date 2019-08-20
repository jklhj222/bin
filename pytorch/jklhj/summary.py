#!/usr/bin/env python3.6

from torchsummary import summary
from transformer_net import TransformerNet
from torchvision.models import vgg16

model = TransformerNet()
vgg = vgg16()

print(summary(model, input_size=(3, 192, 156), device='cpu'))
