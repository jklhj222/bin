#!/usr/bin/env python3

import cv2

def images2hdr(imgs):
    merge_mertens = cv2.createMergeMertens()

    fusion = merge_mertens.process(imgs)

    return fusion * 255


if __name__ == '__main__': 

    for i in range(1, 3):
        imgs = []
        for j in [50000, 20000, 10000, 5000, 2000, 1000]:
            imgs.append('frame{:05d}_{}.jpg'.format(i, j))

        images = [cv2.imread(img) for img in imgs]
        img_fusion = images2hdr(images)

        cv2.imwrite('frame{:05d}_fusion.jpg'.format(i), img_fusion)




#    img_fusion = images2hdr(images)
#    cv2.imwrite('fusion.jpg', img_fusion)
