#!/urs/bin/env python3

import caffe

solver = caffe.SGDSolver('solver.prototxt')
solver.step(1)
