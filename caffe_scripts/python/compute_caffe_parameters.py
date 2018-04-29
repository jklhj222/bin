#!/usr/bin/env python3

import caffe
caffe.set_mode_gpu()
import numpy as np
from numpy import prod, sum
from pprint import pprint

def print_net_parameters (deploy_file):
    print("Net: " + deploy_file)
    net = caffe.Net(deploy_file, caffe.TEST)
    print("Layer-wise parameters: ")
    pprint([(k, v[0].data.shape) for k, v in list(net.params.items())])
    print( "Total number of parameters: " + 
      str( format(sum( [prod(v[0].data.shape) for k, v in list(net.params.items())] ),',') ) )

input_file = input("deploy file name: ")
    
deploy_file = input_file
print_net_parameters(deploy_file)

# Sample output:
# Net: /home/ubuntu/deploy.prototxt
# Layer-wise parameters: 
#[('conv1', (96, 3, 11, 11)),
# ('conv2', (256, 48, 5, 5)),
# ('conv3', (384, 256, 3, 3)),
# ('conv4', (384, 192, 3, 3)),
# ('conv5', (256, 192, 3, 3)),
# ('fc6', (4096, 9216)),
# ('fc7', (4096, 4096)),
# ('fc8', (819, 4096))]
# Total number of parameters: 60213280
