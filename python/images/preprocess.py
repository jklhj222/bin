#!/usr/bin/env python3

import cv2
import numpy as np

def fft2Image(src):
    r, c = src.shape[:2]
    rPadded = cv2.getOptimalDFTSize(r)
    cPadded = cv2.getOptimalDFTSize(c)

    fft2 = np.zeros((rPadded, cPadded, 2), np.float32)

    fft2[:r, :c, 0] = src

    cv2.dft(fft2, fft2, cv2.DFT_COMPLEX_OUTPUT)

    return fft2


def preprocess(img_file, resize=None):
    img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    print('img.shape: ', img.shape)

    variance = np.var(img/255)
    std = np.std(img/255)
    print('variance: ', variance, 'std: ', std)

    height, width = img.shape

    if resize is not None:
        img = cv2.resize(img, (int(width*resize[0]), int(height*resize[1])))
        print('img resize:', img.shape)

    # fft
    fft2 = fft2Image(img)
    amp = np.sqrt(np.power(fft2[:,:,0], 2.0) + np.power(fft2[:,:,1], 2.0))
    amp = np.log(amp + 1.0)
    spectrum = np.zeros(amp.shape, np.float32)
    cv2.normalize(amp, spectrum, 0, 1, cv2.NORM_MINMAX)

    # Gaussian Blur
    img_gauss = cv2.GaussianBlur(img, (5, 5), 0)

    # Adaptive threshold
    img_adap = cv2.adaptiveThreshold(img,
                                     255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY,
                                     151,
                                     5)

    # median filter to remove salt-and-pepper noise
    img_adap = cv2.medianBlur(img_adap, 7)

    # OTSU thresholding
    ret, img_otsu = cv2.threshold(img, 50, 255, cv2.THRESH_OTSU)

    return img, img_adap, img_otsu, img_gauss, spectrum

def plot(imgs, figsize, subplot, savefig=None):
    plt.figure(num='test',figsize=figsize)

    for i, img in enumerate(imgs):
        if i==0: 
            subplot.append(i+1)
        else:
            subplot[2] = i+1

        plt.subplot(subplot[0], subplot[1], subplot[2])

        plt.title(img) 

        plt.imshow(imgs[img], cmap=plt.cm.gray)

        plt.axis('off')

    if savefig is not None: plt.savefig(savefig)

    plt.show()


if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt
    import collections

    parser = argparse.ArgumentParser()

    parser.add_argument('--img_file', default=None)

    args = parser.parse_args()

    img_file = args.img_file 
 
    img, img_adap, img_otsu, img_gauss, spectrum = preprocess(img_file, resize=(3.0, 3.0)) 

    imgs_list = [('Original', img), 
                 ('adap', img_adap),
                 ('otsu', img_otsu),
                 ('gauss', img_gauss),
                 ('fft', spectrum)]

    imgs = collections.OrderedDict(imgs_list)

    plot(imgs, (8, 8), [3, 3])

