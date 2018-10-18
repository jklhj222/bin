# imports
import json
import time
import pickle
import scipy.misc
import skimage.io
import caffe
import csv

import numpy as np
import os.path as osp

from xml.dom import minidom
from random import shuffle
import random
from threading import Thread
from PIL import Image

from tools import SimpleTransformer


class MultilabelDataLayerSync(caffe.Layer):

    """
    This is a simple synchronous datalayer for training a multilabel model.
    """

    def setup(self, bottom, top):

        self.top_names = ['data', 'label']

        # === Read input parameters ===

        # params is a python dictionary with layer parameters.
        params = eval(self.param_str)

        # Check the parameters for validity.
        check_params(params)

        # store input as class variables
        self.batch_size = params['batch_size']

        # The number of classes
        self.number_classes = params['number_classes']

        # The extension of the images
        self.img_ext = params['img_ext']

        # Create a batch loader to load the images.
        self.batch_loader = BatchLoader(params, None)

        # === reshape tops ===
        # since we use a fixed input image size, we can shape the data layer
        # once. Else, we'd have to do it in the reshape call.
        top[0].reshape(
            self.batch_size, 3, params['im_shape'][0], params['im_shape'][1])
        # the label shape.
        top[1].reshape(self.batch_size, self.number_classes)

        print_info("MultilabelDataLayerSync", params)

    def forward(self, bottom, top):
        """
        Load data.
        """
        for itt in range(self.batch_size):
            # Use the batch loader to load the next image.
            im, multilabel = self.batch_loader.load_next_image()

            # Add directly to the caffe data layer
            top[0].data[itt, ...] = im
            top[1].data[itt, ...] = multilabel

    def reshape(self, bottom, top):
        """
        There is no need to reshape the data, since the input is of fixed size
        (rows and columns)
        """
        pass

    def backward(self, top, propagate_down, bottom):
        """
        These layers does not back propagate
        """
        pass


class BatchLoader(object):

    """
    This class abstracts away the loading of images.
    Images can either be loaded singly, or in a batch. The latter is used for
    the asyncronous data layer to preload batches while other processing is
    performed.
    """

    def __init__(self, params, result):
        self.result = result
        self.batch_size = params['batch_size']
        self.number_classes = params['number_classes']
        self.img_ext = params['img_ext']
        self.dataset_root = params['dataset_root']
        self.im_shape = params['im_shape']

        # get list of image indexes.
        list_file = params['split'] + '.csv'
        self.indexlist = [line.rstrip('\n').split(',')[0] for line in open(
            osp.join(self.dataset_root, list_file))]
        self.labellist = [line.rstrip('\n').split(',')[1] for line in open(
            osp.join(self.dataset_root, list_file))]
        
        self._cur = 0  # current image
        # this class does some simple data-manipulations
        self.transformer = SimpleTransformer()

        print("BatchLoader initialized with {} images".format(
            len(self.indexlist)))

    def load_next_image(self):
        """
        Load the next image in a batch.
        """
        # Did we finish an epoch?
        if self._cur == len(self.indexlist):
            self._cur = 0
            randnum = random.randint(0,100)
            random.seed(randnum)
            shuffle(self.indexlist)
            random.seed(randnum)
            shuffle(self.labellist)

        # Load an image
        index = self.indexlist[self._cur]  # Get the image index
        image_file_name = index + self.img_ext
        im = np.asarray(Image.open(
            osp.join(self.dataset_root, 'images', image_file_name)))
        im = scipy.misc.imresize(im, self.im_shape)  # resize

        # do a simple horizontal flip as data augmentation
        flip = np.random.choice(2)*2-1

        im = im[:, ::flip, :]

        # Load and prepare ground truth
        multilabel = np.zeros(self.number_classes).astype(np.float32)
        for label in self.labellist[self._cur].split(' '):
            multilabel[int(label)] = 1
                
        self._cur += 1
        return self.transformer.preprocess(im), multilabel


def check_params(params):
    """
    A utility function to check the parameters for the data layers.
    """
    assert 'split' in params.keys(
    ), 'Params must include split (train, val, or test).'

    required = ['batch_size', 'dataset_root', 
                'im_shape', 'number_classes', 'img_ext']
    for r in required:
        assert r in params.keys(), 'Params must include {}'.format(r)


def print_info(name, params):
    """
    Output some info regarding the class
    """
    print("{} initialized for split: {}, with bs: {}, "
          "im_shape: {}, number_classes: {}, img_ext: {}".format(name,
                                                params['split'],
                                                params['batch_size'],
                                                params['im_shape'],
                                                params['number_classes'],
                                                params['img_ext']))
