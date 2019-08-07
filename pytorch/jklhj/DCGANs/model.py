#!/usr/bin/env python3

from torch import nn

class NetG(nn.Module):
    def __init__(self, config):
        super(NetG, self).__init__()
        self.ngf = config.ngf
        self.nz = config.nz
        ngf = self.ngf
        nz = self.nz

        self.main = nn.Sequential(
          nn.ConvTranspose2d(nz, ngf*8, 4, 1, 0, bias=False),
          nn.BatchNorm2d(ngf*8),
          nn.ReLU(inplace=True),
          # output shape: (ngf*8, 4, 4)

          nn.ConvTranspose2d(ngf*8, ngf*4 , 4, 2, 1, bias=False),
          nn.BatchNorm2d(ngf*4),
          nn.ReLU(inplace=True),
          # output shape: (ngf*4, 8, 8)

          nn.ConvTranspose2d(ngf*4, ngf*2, 4, 2, 1, bias=False),
          nn.BatchNorm2d(ngf*2),
          nn.ReLU(inplace=True),
          # output shape: (ngf*2, 16, 16)

          nn.ConvTranspose2d(ngf*2, ngf, 4, 2, 1, bias=False),
          nn.BatchNorm2d(ngf),
          nn.ReLU(inplace=True),
          # output shape: (ngf, 32, 32)

          nn.ConvTranspose2d(ngf, 3, 5, 3, 1, bias=False),
          nn.Tanh() # range of output between -1 ~ 1
          # output shape: (3, 96, 96)
        )

    def forward(self, Input):
        return self.main(Input)


class NetD(nn.Module):
    def __init__(self, config):
        super(NetD, self).__init__()
        self.ndf = config.ndf
        self.nz = config.nz
        ndf = self.ndf
        nz = self.nz

        self.main = nn.Sequential(
          # input shape: (3, 96, 96)
          nn.Conv2d(3, ndf, 5, 3, 1, bias=False),
          nn.LeakyReLU(negative_slope=0.2, inplace=True),
          # output shape: (ndf, 32, 32)

          nn.Conv2d(ndf, ndf*2, 4, 2, 1, bias=False),
          nn.BatchNorm2d(ndf*2),
          nn.LeakyReLU(negative_slope=0.2, inplace=True),
          # output shape: (ndf*2, 16, 16)

          nn.Conv2d(ndf*2, ndf*4, 4, 2, 1, bias=False),
          nn.BatchNorm2d(ndf*4),
          nn.LeakyReLU(negative_slope=0.2, inplace=True),
          # output shape: (ndf*4, 8, 8)

          nn.Conv2d(ndf*4, ndf*8, 4, 2, 1, bias=False),
          nn.BatchNorm2d(ndf*8),
          nn.LeakyReLU(negative_slope=0.2, inplace=True),
          # output shape: (ndf*8, 4, 4)

          nn.Conv2d(ndf*8, 1, 4, 1, 0, bias=False),
          nn.Sigmoid() # output probability
        )

    def forward(self, Input):
        return self.main(Input).view(-1)
