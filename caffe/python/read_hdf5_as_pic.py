#!/usr/bin/env python3
""" Created on Mon Aug 13 14:36:13 2018 @author: jklhj """

import h5py
from PIL import Image
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='To read hdf5 file and show the picture in it.')

parser.add_argument('--h5_file',
                    help='h5_file is the hdf5 file for reading.')

parser.add_argument('--index_of_pic',
                    help='index_of_pic is the index of picture in hdf5 file',
                    default=0,
                    type=int)

parser.add_argument('--show_pic_false',
                    help='set False to show the picture from PIL',
                    action='store_false')

args = parser.parse_args()

def read_hd5f_as_pic(h5_file=None, 
                     index_of_pic=None,
                     show_pic_false=None):
    
    f = h5py.File(h5_file, 'r')
    
    label = f['label']
    data  = f['data']
    
    pic = np.array( data[index_of_pic]*255 )
    
    pic = np.uint8(pic)
    
    pic = np.transpose(pic)
    
    im = Image.fromarray( pic )
    
    print('label: ', label[index_of_pic])
    
    if show_pic_false: im.show()
    
if __name__ == '__main__':
    
    read_hd5f_as_pic(h5_file=args.h5_file,
                     index_of_pic=args.index_of_pic,
                     show_pic_false=args.show_pic_false)
#    read_hd5f_as_pic(h5_file='train.h5',
#                     index_of_pic=0,
#                     show_pic_false=True)
