#!/usr/bin/env python3

import numpy as np
import struct
import matplotlib.pyplot as plt

filename = 'train-images-idx3-ubyte'
with open(filename,'rb') as f1:
    buf1 = f1.read() 

image_index = 0
image_index += struct.calcsize('>IIII')
temp = struct.unpack_from('>784B', buf1, image_index) 
# '>784B'的意思就是用大端法读取784( 28*28 )个unsigned byte

im = np.reshape(temp,(28,28))
plt.imshow(im , cmap='gray')
plt.show()
