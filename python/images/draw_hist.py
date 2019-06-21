#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt

def plot_gray_hist(img_file, savefig=None):
    img = cv2.imread(img_file)

    # to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    plt.figure()

    plt.title('Grayscale Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')

    plt.plot(hist)

    plt.xlim([0, 256])

    if savefig is not None: plt.savefig(savefig)

    plt.show()

    cv2.waitKey(0)

def plot_color_hist(img_file, savefig=None):
    img = cv2.imread(img_file)

    chanls = cv2.split(img)

    colors = ('b', 'g', 'r')

    plt.figure()

    plt.title('Color Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')

    for (chanl, color) in zip(chanls, colors):
        hist = cv2.calcHist([chanl], [0], None, [256], [0, 256])

        plt.plot(hist, color=color)

        plt.xlim([0, 256])
       
    if savefig is not None: plt.savefig(savefig)

    plt.show()

    cv2.waitKey(0)


def plot_gray_bar(img_file, savefig=None):
    img = cv2.imread(img_file)

    # to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.reshape(256)

    plt.figure()

    plt.title('Grayscale Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')

    plt.bar(range(1, 257), hist)

    plt.xlim([0, 256])

    if savefig is not None: plt.savefig(savefig)

    plt.show()

    cv2.waitKey(0)


def plot_color_bar(img_file, savefig=None):
    img = cv2.imread(img_file)

    chanls = cv2.split(img)

    colors = ('b', 'g', 'r')

    plt.figure()

    plt.title('Color Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')

    for (chanl, color) in zip(chanls, colors):
        hist = cv2.calcHist([chanl], [0], None, [256], [0, 256])
        hist = hist.reshape(256)

        plt.bar(range(1, 257), hist, color=color)

        plt.xlim([0, 256])
       
    if savefig is not None: plt.savefig(savefig)

    plt.show()

    cv2.waitKey(0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
               description='To show the histogram of the picture.')

    parser.add_argument('--img_file', default=None)

    args = parser.parse_args()

    plot_gray_hist(args.img_file)
#    plot_color_hist(args.img_file)
#    plot_gray_bar(args.img_file)
#    plot_color_bar(args.img_file)

