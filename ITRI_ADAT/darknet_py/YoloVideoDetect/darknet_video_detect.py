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

parser.add_argument('--cfg_file', default='config.txt')

parser.add_argument('--resize', default=1.0)

parser.add_argument('--gpu_idx', default='0')

parser.add_argument('--save_video', default=False, action='store_true')

parser.add_argument('--thresh', default=0.25)

args = parser.parse_args()

#cfg_file = 'config.txt'
cfg_file = args.cfg_file
config = configparser.RawConfigParser()
config.read(cfg_file)

cap = cv2.VideoCapture(args.video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * float(args.resize))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * float(args.resize))
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
                           thresh=float(args.thresh))

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    return objs

fourcc = cv2.VideoWriter_fourcc(*'XVID')

if args.save_video:
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (width, height))

ii=0
while (cap.isOpened()):
    ii+=1
    ret, frame = cap.read()
    print('frame type: ', ii, ret, type(frame))
    if not ret:
        break

#    frame = cv2.resize( frame, (int(frame.shape[1]*float(args.resize)), 
#                                int(frame.shape[0]*float(args.resize))) )

    frame = cv2.resize( frame, (width, height))

    cv2.imwrite('tmp.jpg', frame)
 
    objs = yolo_img_detect('tmp.jpg', net, meta, darknet_data)

    new_objs = [obj for obj in objs if obj.name != 'background']
    for obj in objs:
        print('obj: ', obj.name, obj.conf)

    img = YoloObj.DrawBBox(objs, frame, show=False, save=False)

    if args.save_video:
        out.write(img)

    cv2.imshow('frame', img)

    k = cv2.waitKey(1) & 0xFF

    if k == 27 or k== ord('q'):
        break

print('predict finished.')

cap.release()
cv2.destroyAllWindows()
