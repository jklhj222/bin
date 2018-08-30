#!/usr/bin/env python3
## http://nbviewer.jupyter.org/github/BVLC/caffe/blob/master/examples/01-learning-lenet.ipynb
""" Created on Thu Aug 30 10:07:18 2018 @author: jklhj """

### define solver
from caffe.proto import caffe_pb2
s = caffe_pb2.SolverParameter()

import caffe
from caffe import layers as L
from caffe import params as P
import os

TRAIN_NET_PATH = './train.prototxt'
TEST_NET_PATH = './test.prototxt'
SOLVER_CONFIG_PATH = './solver.prototxt'

TRAIN_LMDB_PATH = './mnist_train_lmdb'
TRAIN_BATCH_SIZE = 64
TEST_LMDB_PATH = './mnist_test_lmdb'
TEST_BATCH_SIZE = 100

def solver_creator(train_net_path,
                   test_net_path,
                   solver_config_path):
    
    # Set a seed for reproducible experiments:
    # this controls for randomization in training.
    s.random_seed = 0xCAFFE
    
    # Specify locations of the train and (maybe) test networks.
    s.train_net = train_net_path
    s.test_net.append(test_net_path)
    s.test_interval = 500  # Test after every 500 training iterations.
    s.test_iter.append(100) # Test on 100 batches each time we test.
    
    s.max_iter = 10000     # no. of times to update the net (training iterations)
     
    # EDIT HERE to try different solvers
    # solver types include "SGD", "Adam", and "Nesterov" among others.
    s.type = "SGD"
    
    # Set the initial learning rate for SGD.
    s.base_lr = 0.01  # EDIT HERE to try different learning rates
    # Set momentum to accelerate learning by
    # taking weighted average of current and previous updates.
    s.momentum = 0.9
    # Set weight decay to regularize and prevent overfitting
    s.weight_decay = 5e-4
    
    # Set `lr_policy` to define how the learning rate changes during training.
    # This is the same policy as our default LeNet.
    s.lr_policy = 'inv'
    s.gamma = 0.0001
    s.power = 0.75
    # EDIT HERE to try the fixed rate (and compare with adaptive solvers)
    # `fixed` is the simplest policy that keeps the learning rate constant.
    # s.lr_policy = 'fixed'
    
    # Display the current training loss and accuracy every 1000 iterations.
    s.display = 1000
    
    # Snapshots are files used to store networks we've trained.
    # We'll snapshot every 5K iterations -- twice during training.
    s.snapshot = 5000
    s.snapshot_prefix = 'mnist/custom_net'
    
    # Train on the GPU
    s.solver_mode = caffe_pb2.SolverParameter.GPU
    
    # Write the solver to a temporary file and return its filename.
    if os.path.exists(solver_config_path):
        yn = input('the solver file exists, deleted it? (y/n) '
                   '(default: y) ') or 'y'
        if yn == 'y': 
            os.remove(solver_config_path)
        else:
            print("the solver file didn't be deleted.")
    
    with open(solver_config_path, 'w') as f:
        f.write(str(s))

def net_creator(lmdb_path, 
                batch_size,
                net_path):
    # define your own net!
    n = caffe.NetSpec()
    
    # keep this data layer for all networks
    n.data, n.label = L.Data( batch_size=batch_size, 
                              backend=P.Data.LMDB, 
                              source=lmdb_path,
                              transform_param=dict(scale=1./255), ntop=2 )
    
    # EDIT HERE to try different networks
    # this single layer defines a simple linear classifier
    # (in particular this defines a multiway logistic regression)
    n.score =   L.InnerProduct(n.data, num_output=10, weight_filler=dict(type='xavier'))
    
    # EDIT HERE this is the LeNet variant we have already tried
    n.conv1 = L.Convolution(n.data, kernel_size=5, num_output=20, weight_filler=dict(type='xavier'))
    # n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    # n.conv2 = L.Convolution(n.pool1, kernel_size=5, num_output=50, weight_filler=dict(type='xavier'))
    # n.pool2 = L.Pooling(n.conv2, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    # n.fc1 =   L.InnerProduct(n.pool2, num_output=500, weight_filler=dict(type='xavier'))
    # EDIT HERE consider L.ELU or L.Sigmoid for the nonlinearity
    # n.relu1 = L.ReLU(n.fc1, in_place=True)
    # n.score =   L.InnerProduct(n.fc1, num_output=10, weight_filler=dict(type='xavier'))
    
    # keep this loss layer for all networks
    n.loss =  L.SoftmaxWithLoss(n.score, n.label)
    
    if os.path.exists(net_path):
        yn = input('the net file exists, deleted it? (y/n) (default: y) ') or 'y'
        if yn == 'y': 
            os.remove(net_path)
        else:
            print("the net file didn't be deleted.")

    with open(net_path, 'w') as f:
        f.write( str(n.to_proto()) )    


if __name__ == '__main__':
    
    solver_creator(TRAIN_NET_PATH,
                   TEST_NET_PATH,
                   SOLVER_CONFIG_PATH)
    
    net_creator(TRAIN_LMDB_PATH,
                TRAIN_BATCH_SIZE,
                TRAIN_NET_PATH)
