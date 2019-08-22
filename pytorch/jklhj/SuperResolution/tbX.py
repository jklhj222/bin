#!/usr/bin/env python3.6

import tensorboardX 
import torch
from torchvision.models import resnet34
import torch.onnx

x=torch.autograd.Variable(torch.rand(1,3,224,224)) #随便定义一个输入
model=resnet34()
writer=tensorboardX.SummaryWriter("./logs/")  #定义一个tensorboardX的写对象 
writer.add_graph(model,x,verbose=True)  #将proto格式的文件转换为tensorboard中的graph
