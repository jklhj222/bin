#!/urs/bin/env python3

import cv2
import os
import time
import shutil
import datetime
import YoloObj 
import DarknetFunc as DFUNC
import configparser

def get_last_file(data_dir):
    # list all the files in data_dir
    files = os.listdir(data_dir)
    # sort the files by time
    files.sort(key=lambda x:os.path.getmtime(os.path.join(data_dir,x)))

    if len(files) != 0:
        #get the newest file
        time = datetime.datetime.fromtimestamp(
                 os.path.getmtime(os.path.join(data_dir, files[-1])))
        #get the directory of the file
        path = os.path.join(data_dir, files[-1])
     
#        print('the newest file is: ' + files[-1])
#        print('time：' + time.strftime('%Y-%m-%d %H-%M-%S'))

        return (path, files[-1])

    else:
        print('the ~DATA_DIR/images directory is empty.')

def get_last_2file(data_dir):
    # list all the files in data_dir
    files = os.listdir(data_dir)

    # sort the files by time
    files.sort(key=lambda x:os.path.getmtime(os.path.join(data_dir,x)))

    if len(files) >= 2:
        time = datetime.datetime.fromtimestamp(
                 os.path.getmtime(os.path.join(data_dir, files[-2])))

        #get the 2nd-newest file
        path = os.path.join(data_dir, files[-2])

        if len(files) > 50:
            os.remove(os.path.join(data_dir, files[0]))

        return (path, files[-2])
        

if __name__ == '__main__':
    cfg_file = 'config.txt'
    config = configparser.RawConfigParser()
    config.read(cfg_file)

    # Read the configurations 
    data_dir = config['DATA']['DATA_DIR']
    imgs_dir = os.path.join(data_dir, 'images')
    flip_dir = os.path.join(data_dir, 'flip_images')
    res_file = config['DATA']['RES_FILE']
    out_file = os.path.join(data_dir, res_file)

    darknet_cfg = config['DARKNET']['CFG']
    darknet_weights = config['DARKNET']['WEIGHTS']
    darknet_data = config['DARKNET']['DATA_FILE']

    topdown_flip = eval(config['DARKNET']['TOPDOWN_FLIP'])
    show_img = eval(config['DARKNET']['SHOW_IMG'])
    save_img = eval(config['DARKNET']['SAVE_IMG'])

    if os.path.exists(imgs_dir):
        shutil.rmtree( os.path.abspath(os.path.abspath(imgs_dir)) )
    if os.path.exists(flip_dir):
        shutil.rmtree( os.path.abspath(os.path.abspath(flip_dir)) )

    os.mkdir(imgs_dir)
    if topdown_flip: os.mkdir(flip_dir)

    if os.path.exists(out_file):
        rmfile = input('the output file "' +  out_file + '" is existed.'
                       'remove it? (y/n)')
        if rmfile == 'Y' or "y": os.remove(out_file)

    # Load the net, weights, and cfg files for darkent
    net = DFUNC.load_net(bytes(darknet_cfg, 'utf-8'), bytes(darknet_weights, 'utf-8'), 0)
    meta = DFUNC.load_meta(bytes(darknet_data, 'utf-8'))

    file_tmp = None 
    while True:
        # Find the 2nd-newest image sent to image directory
        if len(os.listdir(imgs_dir)) >= 2 and file_tmp != get_last_2file(imgs_dir)[0]:
            print('file_tmp, last_file: ', file_tmp, get_last_2file(imgs_dir)[0])
#            img_path, filename = get_last_file(imgs_dir)
            (img_path, filename) = get_last_2file(imgs_dir)
            print('img_path, filename: ', img_path, filename)

            if topdown_flip or show_img or save_img:
                img = cv2.imread(img_path)
                if topdown_flip: 
                    img = cv2.flip(img, 0)
                    cv2.imwrite(os.path.join(flip_dir, filename), img)
                    results = DFUNC.detect(net, 
                                           meta, 
                                           bytes(os.path.join(flip_dir, 
                                                              filename), 
                                                 encoding='utf-8'))

                    # remove the oldest file 
                    # if the number of images > 50 in flip_dir
                    get_last_2file(flip_dir)

            else:
                results = DFUNC.detect(net, 
                                       meta, 
                                       bytes(img_path, encoding='utf-8'))
 

            print('results:', results, len(results), '\n')
            file_tmp = img_path            

            # If nothing to be detected, 
            # write the empty string to output file and skip the loop
            if len(results) == 0:
                YoloObj.WriteToFile(img_path, out_file, [])

                continue
                
            out = []
            objs = []
            for result in results:
                obj = YoloObj.DetectedObj(result)
                objs.append(obj)
                print('\nobjstring', obj.obj_string)

            # Do the In-Out calculation or not
            if eval(config['INOUT_DETECT']['INOUT_DETECT']):
                inout_pairs = eval(config['INOUT_DETECT']['INOUT_PAIRS'])
                poi_thresh = float(config['INOUT_DETECT']['POI_THRESH'])

                OutObjs = YoloObj.DetectedObj.CalcInOutObj(inout_pairs, 
                                                           poi_thresh, 
                                                           objs) 

                for innerName, outerName in inout_pairs:
                    innerObjs = [obj for obj in objs if obj.name == innerName]
                    outerObjs = [obj for obj in objs if obj.name == outerName]
                
                print('innerObjs:', innerObjs, len(innerObjs))
                print('outerObjs:', outerObjs, len(outerObjs))
                print('len(OutObjs): ', len(OutObjs), len(innerObjs), len(outerObjs))

                # If nothing to be detected in in-out detection mode, 
                # write the empty string to output file and skip the loop
                if len(OutObjs)==0 or len(innerObjs)==0 or len(outerObjs)==0:
                    YoloObj.WriteToFile(img_path, out_file, [])

                    continue

                else:
                    YoloObj.WriteToFile(img_path, out_file, OutObjs)
                    
                if show_img or save_img: 
                    YoloObj.DrawBBox(OutObjs,img,show=show_img,save=save_img)
                 
            else:    
                YoloObj.WriteToFile(img_path, out_file, objs)

                if show_img or save_img: 
                    YoloObj.DrawBBox(objs, img, show=show_img, save=save_img)
                
                print('out:', out, '\n')
                print(len(results), '\n')

        else:
            print('waiting for the next image ...', end='\r')


