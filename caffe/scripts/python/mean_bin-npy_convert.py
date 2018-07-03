#!/usr/bin/env python3
#http://www.cnblogs.com/denny402/p/5102328.html
# usage : 
# python3 ./mean_bin-npy_convert.py  filename_of_mean.binaryprotoi(build from compute_image_mean)  filename_of_mean.npy
import numpy as np
import sys,caffe

if len(sys.argv)!=3:
    print("Usage: python3 mean_bin-npy_convert.py mean.binaryproto mean.npy")
    sys.exit()

blob = caffe.proto.caffe_pb2.BlobProto()
bin_mean = open( sys.argv[1] , 'rb' ).read()
blob.ParseFromString(bin_mean)
arr = np.array( caffe.io.blobproto_to_array(blob) )
npy_mean = arr[0]
np.save( sys.argv[2] , npy_mean )

