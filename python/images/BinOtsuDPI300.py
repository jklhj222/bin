#!/usr/bin/env python3


from PIL import Image
import cv2

def ImgBinarize(img_file, out_file):
    img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)

    ret, img_otsu = cv2.threshold(img, 50, 255, cv2.THRESH_OTSU)

    img_otsu = Image.fromarray(img_otsu)

    img_otsu.save(out_file, dpi=(300, 300))

    return img, (ret, img_otsu)


if __name__ == '__main__':    

    img_file = '9988394539043_cut.png'

    out_file = '9988394539043_cut_BinDPI300.png'

    ImgBinarize(img_file, out_file)
