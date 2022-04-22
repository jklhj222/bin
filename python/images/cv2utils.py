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


def fullTest(img, func_list):
    # func_list: [
    #             ('gray', cv2.cvtColor, [cv2.COLOR_BGR2GRAY], {}),
    #             ('contrast_bright: b0, c50', ContrastBrightness, [], {'brightness': 0 , 'contrast': 50}),
    #              ...
    #            ]

    import copy
    func_list_ = copy.deepcopy(func_list)
    img_orig = img.copy()

    result_list = []
    result_list.append(('original', img))
    for func in func_list_:
        f_name = func[0]
        f = func[1]
        args = func[2]
        kargs = func[3]

        args.insert(0, img)
        img = f(*args, **kargs)

        result_list.append((f_name, img))

    return result_list


def zoomin(img_f, scale=2.5, cut_size=(768, 432)):
    img = cv2.imread(img_f)

    h, w, c = img.shape
    hz = int(h * 2.5)
    wz = int(w * 2.5)
    print(h*scale, w*scale)

    img_z = cv2.resize(img, (wz, hz), 
                       interpolation=cv2.INTER_AREA)

    img_crop = img_z[int((hz/2)-(cut_size[1]/2)):int((hz/2)+(cut_size[1]/2)),
                     int((wz/2)-(cut_size[0]/2)):int((wz/2)+(cut_size[0]/2))]

#    cvshow(img_crop)

    return img_crop

