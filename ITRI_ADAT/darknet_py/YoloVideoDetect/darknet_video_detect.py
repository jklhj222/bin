#!/usr/bin/env python3

import cv2
import time
import configparser
import argparse
import DarknetFunc as DFUNC
import YoloObj
import cv2
import os

parser = argparse.ArgumentParser()

parser.add_argument('--video_path', default=None)

parser.add_argument('--resize', default=1.0)

parser.add_argument('--gpu_idx', default='0')

args = parser.parse_args()

cfg_file = 'config.txt'
config = configparser.RawConfigParser()
config.read(cfg_file)

cap = cv2.VideoCapture(args.video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps:', fps)

darknet_cfg = config['DARKNET']['CFG']
darknet_weights = config['DARKNET']['WEIGHTS']
darknet_data = config['DARKNET']['DATA_FILE']

os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_idx
print(os.environ['CUDA_VISIBLE_DEVICES'])

net = DFUNC.load_net(bytes(darknet_cfg, 'utf-8'), bytes(darknet_weights, 'utf-8'), 0)
meta = DFUNC.load_meta(bytes(darknet_data, 'utf-8'))

def yolo_img_detect(img, net, meta, darknet_data):
    import YoloObj

    results = DFUNC.detect(net, meta, bytes(img, encoding='utf-8'),
                           thresh=0.25)

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    return objs


while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize( frame, (int(frame.shape[1]*float(args.resize)), 
                                int(frame.shape[0]*float(args.resize))) )

    cv2.imwrite('tmp.jpg', frame)
 
    objs = yolo_img_detect('tmp.jpg', net, meta, darknet_data)

    for obj in objs:
        print('obj: ', obj.name, obj.conf)

    img = YoloObj.DrawBBox(objs, frame, show=False, save=False)

    cv2.imshow('frame', img)

    k = cv2.waitKey(1) & 0xFF

    if k == 27 or k== ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
