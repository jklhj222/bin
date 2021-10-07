#!/usr/bin/env python3
import cv2

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
