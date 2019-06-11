#!/usr/bin/env python3

def yolo_img_detect(img, net, meta, darknet_data):
    import YoloObj

    results = DFUNC.detect(net, meta, img)

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    return objs


if __name__ == '__main__':
    import configparser
    import argparse
    import DarknetFunc as DFUNC
    import YoloObj
    import cv2
    import os

    parser = argparse.ArgumentParser()

    parser.add_argument('--img_file', default=None)

    parser.add_argument('--gpu_idx', default='0')

    args = parser.parse_args()

    img_file = args.img_file
    cfg_file = 'config.txt'
    config = configparser.RawConfigParser()
    config.read(cfg_file)

#    img_file = '/home/hugh/Dropbox/tmp/scratch_dent/scratch_20cm/cut4.png'
    img = cv2.imread(img_file)

    # Read the configuraions    
    darknet_cfg = config['DARKNET']['CFG']
    darknet_weights = config['DARKNET']['WEIGHTS']
    darknet_data = config['DARKNET']['DATA_FILE']
    show_img = eval(config['DARKNET']['SHOW_IMG'])
    save_img = eval(config['DARKNET']['SAVE_IMG'])

    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_idx
    print(os.environ['CUDA_VISIBLE_DEVICES'])

    # Load the net, weights, and cfg files for darknet
    net = DFUNC.load_net(bytes(darknet_cfg, 'utf-8'), bytes(darknet_weights, 'utf-8'), 0)
    meta = DFUNC.load_meta(bytes(darknet_data, 'utf-8'))
    
    objs = yolo_img_detect(img, net, meta, darknet_data) 

    for obj in objs:
        print(obj.obj_string, obj.cx, obj.cy)

    print('\nNumber of objects: ', len(objs))

    YoloObj.DrawBBox(objs, img, show_img, save_img)
