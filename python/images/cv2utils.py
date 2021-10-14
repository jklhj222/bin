#!/usr/bin/env python3
import cv2
import matplotlib.pyplot as plt

def cvshow(img, name='test'):
    cv2.imshow(name, img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


def addMask(img, mask):
    mask[:,np.where(mask == 255),0] = 0
    mask[:,np.where(mask == 255),1] = 0

    alpha = 1
    beta = 0.3
    gamma = 0

    mask_img = cv2.addWeighted(img, alpha, mask, beta, gamma)

    return mask_img


def addContours(img, mask):
    img2 = img.copy()

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img2, contours, -1, (0, 0, 255), 3)

    return img2


def bwareaopen(img, size):
    # img: numpy arrary
    # size: windows size. (int)
    output = img.copy()

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)

    for i in range(1, nlabels-1):
        regions_size = stats[i, 4]
        if regions_size < size:
            x0 = stats[i, 0]
            y0 = stats[i, 1]
            x1 = stats[i, 0] + stats[i, 2]
            y1 = stats[i, 1] + stats[i, 3]

            for row in range(y0, y1):
                for col in range(x0, x1):
                    if labels[row, col] == i:
                        output[row, col] = 0

    return output


def plot(imgs, figsize, figname='test', subplot=None, showfig=True, savefig=None):
    # imgs: collections.OrderedDict(imgs_list)
    #       imgs_list = [('original', img), ('gauss', img_gauss), ('absX', absX), ... ]
    # figsize: ex. (6, 6) (tuple)
    # subplot: number of column and row in figure. ex. [4, 3] (list)
    # showfig: True for show figure, False for not show.
    # savefig: None for not saving figure, file name for saving figure. ex. 'test.jpg' (str)

    import numpy as np
    from collections import OrderedDict
    import gc

    imgs = OrderedDict(imgs)
    if subplot is None:
        num_imgs = len(imgs)
        num_rows = np.ceil(np.sqrt(num_imgs))
        num_cols = np.ceil(num_imgs/num_rows)
        subplot = [num_rows, num_cols]

    plt.figure(num=figname, figsize=figsize)

    for i, img in enumerate(imgs):
        if i==0:
            subplot.append(i+1)
        else:
            subplot[2] = i+1

        plt.subplot(int(subplot[0]), int(subplot[1]), int(subplot[2]))

        plt.title(f'{i} : ' + img)

        plt.imshow(imgs[img], cmap=plt.cm.gray)

        plt.axis('off')

    fig = plt.gcf()

    if showfig: plt.show()

    if savefig is not None:
        fig.savefig(savefig)
        plt.clf()
        plt.cla()
        plt.close('all')

        del fig
