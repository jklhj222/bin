#!/usr/bin/env python3

from torchsummary import summary
from model import Darknet53

model = Darknet53()

print(summary(model, input_size=(3, 416, 416), device='cpu'))

#print(len(list(model.parameters())))
