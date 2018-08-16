#!/usr/bin/env python3
# http://www.xieqiang.site/2017/08/10/hdf5-caffe/
""" Created on Mon Aug 13 11:19:03 2018 @author: jklhj """

#import sys
#sys.path.append("../../caffe/python")
import h5py, os
import caffe
import numpy as np
import random
import argparse

#SIZE = 224 # fixed size to all images

parser = argparse.ArgumentParser(
        description='To create the hdf5 file for caffe training.')

parser.add_argument('--label_file',
                    help='the file list with label.')

parser.add_argument('--output_hdf5',
                    help='the output file name of hdf5.')

parser.add_argument('--output_hdf5_list',
                    help='the source for reading for caffe.')

parser.add_argument('--resize',
                    help='the size to transform.',
                    type=int)
 
parser.add_argument('--shuffle_file_false',
                   help='to set without shuffle the files.',
                   default=False,
                   action='store_false')

args = parser.parse_args()


def create_hd5f(label_file=None, 
                output_hdf5=None, 
                output_hdf5_list=None,
                resize=None,
                shuffle_file_false=None):
    
    
    with open( label_file, 'r' ) as T :
        lines = T.readlines()
        if shuffle_file_false: random.shuffle(lines)
        
        data_ = np.zeros( (len(lines), 3, resize, resize), dtype='f4' )
        # for 8 labels
        #label_ = np.zeros( (len(lines), 8), dtype='f4' )
        # for 1 label
        label_ = np.zeros( (len(lines), 1), dtype=np.int8 )
    
         
    for i, l in enumerate(lines):
        sp = l.split(' ')
        img = caffe.io.load_image( sp[0] )
        height, width =  img.shape[0], img.shape[1]
     
        print(i, l, height,width)
        img = caffe.io.resize( img, (resize, resize, 3) ) # resize to fixed size
        img = img.transpose(2,0,1)
         
        # you may apply other input transformations here...
        # Note that the transformation should take img from size-by-size-by-3 and transpose it to 3-by-size-by-size
        data_[i] = img
         
#        # for 8 labels
#        for j in range(8):
#            #The coordinate values for each point are normalized
#            if (j+1)%2:
#                normalize_factor = width
#            else:
#                normalize_factor = height
#            label_[i][j] = float(sp[j+1])/float(normalize_factor)
         
        label_[i] = sp[1]
         
    with h5py.File(output_hdf5,'w') as H:
        H.create_dataset( 'data', data=data_*255 ) # note the name X given to the dataset!
        H.create_dataset( 'label', data=label_ ) # note the name y given to the dataset!
    with open(output_hdf5_list,'w') as L:
        L.write( os.path.join( os.getcwd() + '/' + output_hdf5) ) # list all h5 files you are going to use


if __name__ == '__main__':
    create_hd5f(label_file=args.label_file, 
                output_hdf5=args.output_hdf5, 
                output_hdf5_list=args.output_hdf5_list, 
                resize=args.resize,
                shuffle_file_false=args.shuffle_file_false)    
#    create_hd5f(label_file='train_label.dat',
#                output_hdf5='train.h5',
#                output_hdf5_list='train_h5_list.txt',
#                resize=224,
#                shuffle_file_false=True)
