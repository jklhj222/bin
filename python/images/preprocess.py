#!/usr/bin/env python3

import cv2
import numpy as np
import math

def fft2Image(img):
    r, c = img.shape[:2]
    # find the optimaml rows and columns to fit the vector size 2^p*3^q*5^r
    rPadded = cv2.getOptimalDFTSize(r)
    cPadded = cv2.getOptimalDFTSize(c)

    fft2 = np.zeros((rPadded, cPadded, 2), np.float32)

    fft2[:r, :c, 0] = img

    cv2.dft(fft2, fft2, cv2.DFT_COMPLEX_OUTPUT)

    return fft2


def amplitudeSpectrum(fft2):
    real2 = np.power(fft2[:,:,0], 2.0)
    imag2 = np.power(fft2[:,:,1], 2.0)

    amplitude = np.sqrt(real2 + imag2)

    return amplitude


def graySpectrum(amplitude):
    amplitude = np.log(amplitude + 1.0)
  
    spectrum = np.zeros(amplitude.shape, np.float32)

    cv2.normalize(amplitude, spectrum, 0, 1, cv2.NORM_MINMAX)

    return spectrum


def phaseSpectrum(fft2):
    rows, cols = fft2.shape[:2]

    phase = np.arctan2(fft2[:,:,1], fft2[:,:,0])

    return phase


def specResidual(img):
    fft2 = fft2Image(img)

    amplitude = amplitudeSpectrum(fft2)

    grayAmp = graySpectrum(amplitude)

    phase = phaseSpectrum(fft2)

    cosSpectrum = np.cos(phase)
    sinSpectrum = np.sin(phase)

    meanGrayAmp = cv2.boxFilter(grayAmp, cv2.CV_32FC1, (3, 3))

    specRes = grayAmp - meanGrayAmp

    expSpecRes = np.exp(specRes)

    real = expSpecRes * cosSpectrum
    imag = expSpecRes * sinSpectrum
    
    comp = np.zeros((real.shape[0], real.shape[1], 2), np.float32)
    comp[:,:,0] = real
    comp[:,:,1] = imag

    ifft2 = np.zeros(comp.shape, np.float32)

    cv2.dft(comp, ifft2, cv2.DFT_COMPLEX_OUTPUT + cv2.DFT_INVERSE)

    saliencymap = np.power(ifft2[:,:,0], 2) + np.power(ifft2[:,:,1], 2)

    saliencymap = cv2.GaussianBlur(saliencymap, (11, 11), 2.5)

    cv2.normalize(saliencymap, saliencymap, 0, 1, cv2.NORM_MINMAX)

    saliencymap = saliencymap / np.max(saliencymap)

    saliencymap = np.power(saliencymap, 0.25)
    saliencymap = np.round(saliencymap*255)
    saliencymap = saliencymap.astype(np.uint8)

    return saliencymap, phase 


#def LowPassFilter(shape, center, radius, Type='gauss', n=2):
#    rows, cols = shape[:2]
#
#    r, c = np.

def plot(imgs, figsize, subplot, savefig=None):
    plt.figure(num=img_file,figsize=figsize)

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


def save_imgs(save_imgs):
    for i, save_img in enumerate(save_imgs):
        cv2.imwrite(save_img[0] + '.png', save_img[1])


def preprocess(img_file, resize=None):
    img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    img_inv = 255 - img 
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
    ifft2 = np.zeros(fft2.shape[:2], np.float32)
    cv2.dft(fft2, ifft2, cv2.DFT_REAL_OUTPUT + cv2.DFT_INVERSE + cv2.DFT_SCALE)
    ifft2 = np.copy(ifft2[:img.shape[0], :img.shape[1]])

    amplitude = amplitudeSpectrum(fft2)
    ampSpectrum = graySpectrum(amplitude)
    rows, cols = img.shape
    fimg = np.copy(img)
    fimg = fimg.astype(np.float32)
    for r in range(rows):
        for c in range(cols):
            if (r+c)%2:
                fimg[r][c] = -1*img[r][c]

    fimgfft2 = fft2Image(fimg)
    amSpe = amplitudeSpectrum(fimgfft2)
    graySpe = graySpectrum(amSpe)
    print(graySpe[50, 100])

    graySpe255 = graySpe * 255
    graySpe255 = graySpe255.astype(np.uint8)
    print(graySpe255[50, 100])

    # Gaussian Blur
    img_gauss = cv2.GaussianBlur(img, (9, 9), 0)
    # fft after GaussianBlur
    fft2_gauss = fft2Image(img_gauss)
    amp = np.sqrt(np.power(fft2_gauss[:,:,0], 2.0) + np.power(fft2_gauss[:,:,1], 2.0))
    amp = np.log(amp + 1.0)
    spectrum_gauss = np.zeros(amp.shape, np.float32)
    cv2.normalize(amp, spectrum_gauss, 0, 1, cv2.NORM_MINMAX)

    specRec, phase = specResidual(img)



    # Adaptive threshold
    img_adap = cv2.adaptiveThreshold(img,
                                     255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY,
                                     31,
                                     7)

    inv_adap = cv2.adaptiveThreshold(img_inv,
                                     255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY,
                                     31,
                                     7)

    # median filter to remove salt-and-pepper noise
    img_adap_median = cv2.medianBlur(img_adap, 7)

    # OTSU thresholding
    ret, img_otsu = cv2.threshold(img, 50, 255, cv2.THRESH_OTSU)

    return img, img_inv, img_adap, img_adap_median, inv_adap, \
           img_otsu, img_gauss, fft2, ampSpectrum, spectrum_gauss, \
           fimg, graySpe, graySpe255, specRec, ifft2, phase


if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt
    import collections

    parser = argparse.ArgumentParser()

    parser.add_argument('--img_file', default=None)

    args = parser.parse_args()

    img_file = args.img_file 

    img, img_inv, img_adap, img_adap_median, inv_adap, \
    img_otsu, img_gauss, fft2, ampSpectrum, spectrum_gauss, \
    fimg, graySpe, graySpe255, specRec, ifft2, phase \
      = preprocess(img_file, resize=(1.0, 1.0)) 

    print('phase:', phase.shape)

    imgs_list = [('Original', img), 
                 ('inverse', img_inv),
                 ('adap', img_adap),
                 ('img_adap_median', img_adap_median),
                 ('inv_adap', inv_adap),
                 ('otsu', img_otsu),
                 ('gauss', img_gauss),
#                 ('fft2 gauss'+str(fft2.shape), fft2_gauss[:,:,0]),
#                 ('fft2[1]', fft2[:,:,1]),
                 ('ampSpectrum', ampSpectrum),
                 ('fimg', fimg),
                 ('graySpe', graySpe),
                 ('graySpe255', graySpe255),
                 ('spectrum_gauss', spectrum_gauss),
                 ('specRec', specRec),
                 ('phase', phase),
                 ('ifft2', ifft2)]


    save_imgs_list = [('Original', img), 
                 ('inverse', img_inv),
                 ('graySpe255', graySpe255),
                 ('adap', img_adap),
                 ('img_adap_median', img_adap_median),
                 ('inv_adap', inv_adap),
                 ('otsu', img_otsu),
                 ('gauss', img_gauss),
                 ('ampSpectrum', ampSpectrum*255)]
#                 ('ampSpectrum', img_otsu)]
#                 ('fft2 gauss', fft2_gauss),
#                 ('fft2[1]', fft2[1]),
                 

    if save_imgs_list: save_imgs(save_imgs_list)
    imgs = collections.OrderedDict(imgs_list)

    num_imgs = len(imgs_list)
    num_rows = np.ceil(np.sqrt(num_imgs))
    num_cols = np.ceil(num_imgs/num_rows)

    plot(imgs, (8, 8), [num_rows, num_cols])

