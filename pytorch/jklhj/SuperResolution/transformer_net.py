#!/usr/bin/env python3

import torch as t
import torch.nn as nn
import numpy as np

from config import DefaultConfig as DC

upsample = DC.super_resol_factor

class TransformerNet(nn.Module):
    def __init__(self):
        super(TransformerNet, self).__init__()

        # Downsampling (conv2d with reflection padding)
        self.initial_layers = nn.Sequential(
          ConvLayer(3, 32, kernel_size=9, stride=1),
          nn.InstanceNorm2d(32, affine=True, track_running_stats=True),
          nn.ReLU(inplace=True),
          ConvLayer(32, 64, kernel_size=3, stride=2),
          nn.InstanceNorm2d(64, affine=True, track_running_stats=True),
          nn.ReLU(inplace=True),
          ConvLayer(64, 128, kernel_size=3, stride=2),
          nn.InstanceNorm2d(128, affine=True, track_running_stats=True),
          nn.ReLU(inplace=True)
        )
   
        # Residual layers
        self.res_layers = nn.Sequential(
          ResidualBlock(128),
          ResidualBlock(128),
          ResidualBlock(128),
          ResidualBlock(128),
          ResidualBlock(128)
        )

        # Upsampling 
        self.upsample_layers = nn.Sequential(
          UpsampleConvLayer(128, 64, kernel_size=3, stride=1, 
                            upsample=upsample),

          nn.InstanceNorm2d(64, affine=True, track_running_stats=True),
          nn.ReLU(inplace=True),
          UpsampleConvLayer(64, 32, kernel_size=3, stride=1, 
                            upsample=upsample),

          nn.InstanceNorm2d(32, affine=True, track_running_stats=True),
          nn.ReLU(inplace=True),
          ConvLayer(32, 3, kernel_size=9, stride=1)
        )

    def forward(self, x):
        out = self.initial_layers(x)

        out = self.res_layers(out)

        out = self.upsample_layers(out)

        return out


# Use reflection padding instead of valid 0 padding
class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride):
        super(ConvLayer, self).__init__()
        
        reflection_padding = int(np.floor(kernel_size / 2))

        self.reflection_pad = nn.ReflectionPad2d(reflection_padding)
        
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def forward(self, x):
        out = self.reflection_pad(x)

        out = self.conv2d(out)

        return out


class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()

        self.conv1 = ConvLayer(channels, channels, kernel_size=3, stride=1)
        self.in1 = nn.InstanceNorm2d(channels, affine=True, track_running_stats=True)
        self.conv2 = ConvLayer(channels, channels,kernel_size=3, stride=1)
        self.in2 = nn.InstanceNorm2d(channels, affine=True, track_running_stats=True)
        self.relu = nn.ReLU(inplace=False)

    def forward(self, x):
        residual = x
     
        out1 = self.conv1(x)
        out1 = self.in1(out1)
        out1 = self.relu(out1)

        out2 = self.conv2(out1)
        out2 = self.in2(out2)

        out = out2 + residual

        return out

# Use upsample then Conv2d instead of ConvTranspose2d
# Use reflection padding instead of valid 0 padding
class UpsampleConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, upsample=None):
        super(UpsampleConvLayer, self).__init__()

        self.upsample = upsample
        reflection_padding = int(np.floor(kernel_size / 2))
        self.reflection_pad = nn.ReflectionPad2d(reflection_padding)
        self.conv2d = nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def forward(self, x):
        if self.upsample:
            x = t.nn.functional.interpolate(x, scale_factor=self.upsample)

        out = self.reflection_pad(x)
        out = self.conv2d(out)

        return out


