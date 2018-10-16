#!/usr/bin/env python3

import sys
import os.path as osp

caffe_root = '/home/jklhj/pkg/local/caffe/'
sys.path.append(caffe_root + 'python')
sys.path.append(caffe_root + 'examples/pycaffe/')
sys.path.append(caffe_root + 'examples/pycaffe/layers')

import caffe

# initialize caffe for gpu mode
caffe.set_mode_gpu()
caffe.set_device(0)

solver = caffe.SGDSolver(osp.join('solver.prototxt'))
#solver.net.copy_from(caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel')
#solver.net.copy_from('./pascal_multilabel_snapshot_iter_30000.caffemodel')
solver.restore('./pascal_multilabel_snapshot_iter_30000.solverstate')
solver.test_nets[0].share_with(solver.net)

solver.step(100000)
