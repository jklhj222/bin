#!/usr/bin/env python3

def yolo_img_detect(img, net, meta, darknet_data, gpu_idx=0):
    import YoloObj

    results = DFUNC.detect(net, meta, img)

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    return objs


if __name__ == '__main__':
    import configparser
    import DarknetFunc as DFUNC
    import YoloObj
    import cv2

    cfg_file = 'config.txt'
    config = configparser.RawConfigParser()
    config.read(cfg_file)

    img_file = '2019-01-31_13.03.39.jpg'
    img = cv2.imread(img_file)

    # Read the configuraions    
    darknet_cfg = config['DARKNET']['CFG']
    darknet_weights = config['DARKNET']['WEIGHTS']
    darknet_data = config['DARKNET']['DATA_FILE']


    # Load the net, weights, and cfg files for darknet
    net = DFUNC.load_net(bytes(darknet_cfg, 'utf-8'), bytes(darknet_weights, 'utf-8'), 0)
    meta = DFUNC.load_meta(bytes(darknet_data, 'utf-8'))
    
    objs = yolo_img_detect(img, net, meta, darknet_data, gpu_idx=1) 

    for obj in objs:
        print(obj.obj_string, obj.cx, obj.cy)

    print('\nNumber of objects: ', len(objs))

    YoloObj.DrawBBox(objs, img, show=False, save=True)
