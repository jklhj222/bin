#!/usr/bin/env python3

import torch as t
import torch.nn as nn

from torchsummary import summary

class Darknet53(nn.Module):
    def __init__(self, num_classes=1000, bias=False):
        super(Darknet53, self).__init__()
 
        self.main = nn.Sequential(
          ConvLayer(3, 32, 3, 1, 1, bias=bias),
          
          # Downsample
          ConvLayer(32, 64, 3, 2, 1, bias=bias),

          ResidualBlock(64, 32, 64, bias=bias),

          # Downsample
          ConvLayer(64, 128, 3, 2, 1, bias=bias),
          
          ResidualBlock(128, 64, 128, bias=bias),
          ResidualBlock(128, 64, 128, bias=bias),

          # Downsample
          ConvLayer(128, 256, 3, 2, 1, bias=bias),

          # 8 residual blocks
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),
          ResidualBlock(256, 128, 256, bias=bias),

          # Downsample
          ConvLayer(256, 512, 3, 2, 1, bias=bias),
   
          # 8 residual blocks
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),
          ResidualBlock(512, 256, 512, bias=bias),

          # Downsample
          ConvLayer(512, 1024, 3, 2, 1, bias=bias),

          # 4 residual blocks
          ResidualBlock(1024, 512, 1024, bias=bias),
          ResidualBlock(1024, 512, 1024, bias=bias),
          ResidualBlock(1024, 512, 1024, bias=bias),
          ResidualBlock(1024, 512, 1024, bias=bias),

          # Global average pooling
          nn.AdaptiveAvgPool2d(1),
        )

        # Fully connected
        self.classifier = nn.Sequential(
          nn.Linear(1024 * 1 * 1, 
                    num_classes, 
                    bias=bias)
        )


    def forward(self, x):
        out = self.main(x)

        out = out.view(out.size(0), -1)
        out = self.classifier(out)

        return out


class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, 
                       kernel_size, stride, pad, bias=False):
        super(ConvLayer, self).__init__()

        self.main = nn.Sequential(
          nn.Conv2d(in_channels, out_channels, 
                    kernel_size, stride, pad, bias=bias),
          nn.BatchNorm2d(out_channels, affine=True, track_running_stats=True),
          nn.LeakyReLU(0.1, inplace=True)
        )

    def forward(self, x):
        out = self.main(x) 

        return out


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, 
                       conv1_out_channels, conv2_out_channels, bias=False):
        super(ResidualBlock, self).__init__()

        self.conv1 = ConvLayer(in_channels,
                               conv1_out_channels,
                               1, 1, 0, bias=bias)

        self.conv2 = ConvLayer(conv1_out_channels,
                               conv2_out_channels,
                               3, 1, 1, bias=bias)


    def forward(self, x):
        residual = x

        out1 = self.conv1(x)

        out2 = self.conv2(out1)

        return out2 + residual


if __name__ == '__main__':
    model = Darknet53(num_classes=7, bias=True)

    Input = t.autograd.Variable(t.randn(4, 3, 416, 416)).cuda()
#    print(Input.shape)

#    model.classifier[0] = nn.Linear(1024*1*1, 10, bias=False)

    model.cuda()
#    print(model(Input).shape)

    print(summary(model, input_size=(3, 512, 512), device='cuda'))
#    for i in model.children():
#        print(i, type(i))
#        print()

#    child = list(model.children())

#    print(dir(model))
#    print(model.classifier[0], type(model.classifier[0]))
#    print(child[-1][0], type(child[-1][0]))
#    print(child[-2][-1], type(child))
#    print()
#    print(child[-2][-2], type(child))
#    print(child[-2][-2], type(child[-2][-2]))
