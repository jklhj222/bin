#!/usr/bin/env python3
# 20180506, to show the pictures and corresponding labels from caffe LMDB file

import caffe
import lmdb
import numpy as np
import cv2
from caffe.proto import caffe_pb2

LMDB_DIR = '/mnt/sdb1/work/kaggle/Plant_Seedlings_Classification/origin_data/divide_train_val_90.10/val_data/val_lmdb'

lmdb_env = lmdb.open(LMDB_DIR)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe_pb2.Datum()

for key, value in lmdb_cursor:
    datum.ParseFromString(value)

    label = datum.label
    data = caffe.io.datum_to_array(datum)

    #CxHxW to HxWxC in cv2
    image = np.transpose(data, (1,2,0))
    cv2.imshow('cv2', image)
    cv2.waitKey(1000)
    print('{},{}'.format(key, label))

