#!/usr/bin/env python3
# https://soralab.space-ichikawa.com/2016/12/caffe-ssd-coco/

import sys
sys.path.insert(0, '/home/hugh/pkg/local/caffe_ssd_python2/python/')

from caffe.proto import caffe_pb2
from google.protobuf import text_format

labelmap_file = 'labelmap_coco.prototxt'
f = open(labelmap_file, 'r')

labelmap = caffe_pb2.LabelMap()

text_format.Merge(str(f.read()), labelmap)

num_labels = labelmap.item[35].display_name
#num_labels = len(labelmap.item)

print(num_labels)


def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

print(get_labelname(labelmap, 35))


