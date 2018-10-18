#!/usr/bin/env python3
""" Created on Mon Jul 30 11:47:53 2018 @author: jklhj """

from PIL import Image
from math import floor

class CutImage():

    def cut_img(src_img_path = None, 
                dst_img_dir = None, 
                cut_size_xy = None,
                offset_xy = None,
                save_file = False):
        
        img = Image.open(src_img_path)
        
        x = offset_xy[0]
        y = offset_xy[1]
        xw = x + cut_size_xy[0]
        yh = y + cut_size_xy[1]
        
        region = img.crop( (x, y, xw, yh) )
        
        cut_pic = src_img_path.split('/')[-1].split('.')[0] + '_' \
                           + str(xw - x) + 'x.' + str(yh - y) + 'y.JPG'
            
        region.save(dst_img_dir + cut_pic)
    
        return img.size, region.size
    
    def cut_img_center(src_img_path = None, 
                       dst_img_dir = None, 
                       cut_size_xy = None, 
                       offset_xy = (0, 0),
                       save_file = False):
        
        img = Image.open(src_img_path)
    
        x = floor((img.size[0] - cut_size_xy[0]) / 2) + floor(offset_xy[0]/2)
        y = floor((img.size[1] - cut_size_xy[1]) / 2) + floor(offset_xy[1]/2)
        xw = x + cut_size_xy[0]
        yh = y + cut_size_xy[1]
    
        region = img.crop( (x, y, xw, yh) )
        
        cut_pic = src_img_path.split('/')[-1].split('.')[0] + '_' \
                           + str(xw - x) + 'x.' + str(yh - y) + 'y.JPG'
            
        region.save(dst_img_dir + cut_pic)
    
        return img.size, region.size


class TransformImage():

    def MergeRGB(picR, picG, picB, picOut):
        R = cv2.imread(picR, cv2.IMREAD_GRAYSCALE)
        G = cv2.imread(picG, cv2.IMREAD_GRAYSCALE)
        B = cv2.imread(picB, cv2.IMREAD_GRAYSCALE)

        RGB = cv2.merge([B, G, R])

        cv2.imwrite(picOut, RGB) 
