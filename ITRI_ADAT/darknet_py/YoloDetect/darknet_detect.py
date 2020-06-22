#!/usr/bin/env python3

import cv2
import time
import configparser
import argparse
import DarknetFunc as DFUNC
import YoloObj
import cv2
import os
import copy

parser = argparse.ArgumentParser()

# global parameters
parser.add_argument('--cfg_file', default='config.txt',
                    help='default="config.txt"')

parser.add_argument('--resize', default=1.0, help='default=1.0')

parser.add_argument('--gpu_idx', default='0', help='default=0')

parser.add_argument('--thresh', default=0.25, help='default=0.25')

subparsers = parser.add_subparsers(dest='subparsers', help='img_detect, video_detect')

# parameters for single image detection.
parser_img = subparsers.add_parser('img_detect', 
                                   help='single image detect.')
parser_img.add_argument('--img_path', default=None, 
                        required=True, help='default=None')

parser_img.add_argument('--noshow_img', default=False, 
                        action='store_true', help='default=True')

parser_img.add_argument('--save_img', default=False, 
                        action='store_true', help='default=False')

parser_img.add_argument('--exclude_objs', nargs='+', default='background',
                        help='default="background"')

# parameters for video detection.
parser_video = subparsers.add_parser('video_detect', 
                                     help='video detect.')
parser_video.add_argument('--video_path', default=None, 
                          required=True, help='default=None')

parser_video.add_argument('--save_video', default=False, action='store_true',
                          help='default=False')

parser_video.add_argument('--auto_label', default=False, action='store_true',
                          help='default=False')

parser_video.add_argument('--skip_nolabel', default=False, action='store_true',
                          help='default=False')

parser_video.add_argument('--exclude_objs', nargs='+', default='background',
                          help='default="background"')

args = parser.parse_args()

#cfg_file = 'config.txt'
cfg_file = args.cfg_file
config = configparser.RawConfigParser()
config.read(cfg_file)

darknet_cfg = config['DARKNET']['CFG']
darknet_weights = config['DARKNET']['WEIGHTS']
darknet_data = config['DARKNET']['DATA_FILE']
temp_img_file = config['DARKNET']['TEMP_IMG']
temp_real_size = eval(config['DARKNET']['TEMP_REAL_SIZE'])
temp_objs_coord_file = config['DARKNET']['TEMP_OBJS_COORD']
cam_fov = eval(config['DARKNET']['CAM_FOV'])

os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_idx
print(os.environ['CUDA_VISIBLE_DEVICES'])

net = DFUNC.load_net(bytes(darknet_cfg, 'utf-8'), 
                     bytes(darknet_weights, 'utf-8'), 0)
meta = DFUNC.load_meta(bytes(darknet_data, 'utf-8'))

#filename = os.path.basename(args.video_path)
#dirname = os.path.basename(os.path.dirname(args.video_path))

label_dict = {}
for idx in range(meta.classes):
    label_dict[meta.names[idx]] = idx


def ImgDetect(img_path, net, meta, darknet_data, save_path='./',
              noshow_img=True, save_img=False):

    import YoloObj

    img = cv2.imread(img_path)

    central_ratio = 0.7
    img_central_area = ( (int(img.shape[1]*(1-central_ratio)/2), 
                          int(img.shape[0]*(1-central_ratio)/2)),
                         (int(img.shape[1]*(1-(1-central_ratio)/2)), 
                          int(img.shape[0]*(1-(1-central_ratio)/2))) )

    print('img_central_area: ', img.shape, img_central_area)

    results = DFUNC.detect(net, meta, bytes(img_path, encoding='utf-8'),
                           thresh=float(args.thresh))

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    # for PosMapping()
    if len(objs) > 0:
        objs = sorted(objs, key=lambda x: x.conf, reverse=True)

        objs = [obj for obj in objs if obj.name != '13']
        objs = [obj for obj in objs if obj.cx >= img_central_area[0][0] and obj.cy >= img_central_area[0][1]]
        objs = [obj for obj in objs if obj.cx <= img_central_area[1][0] and obj.cy <= img_central_area[1][1]]

        max_conf_obj = objs[0]

        max_conf_obj_id = label_dict[bytes(max_conf_obj.name, encoding='utf-8')]

    # for CalcOrient()
    if len(objs) > 1:
        max_two_conf_objs = (objs[0], objs[1])

        max_two_conf_objs_id = (label_dict[bytes(max_two_conf_objs[0].name, encoding='utf-8')],
                                label_dict[bytes(max_two_conf_objs[1].name, encoding='utf-8')])

    print('Number of objects: ', len(objs), '\n')

#    temp_img = cv2.imread('C_1200M.jpg')
    temp_img = cv2.imread(temp_img_file)
    
    # template image real size (height, width) in minimeter
#    temp_realsize_mm = (340, 355)
    temp_realsize_mm = temp_real_size

    # camera FOV (vertical, horizontal) in degree
#    cam_fov_deg = (50.0, 64.8)
    cam_fov_deg = cam_fov

    objs_coord = []
#    with open('C_1200M.txt', 'r') as temp_txt:
    with open(temp_objs_coord_file, 'r') as temp_txt:
        temp_coords = temp_txt.readlines()
  
        for temp_coord in temp_coords:
            coord = temp_coord.strip('\n').split()
            
            objs_coord.append( (float(coord[1]), 
                                float(coord[2]), 
                                float(coord[3]), 
                                float(coord[4])) )

    if len(objs) > 1:
        two_temp_objs_coord = (objs_coord[max_two_conf_objs_id[0]],
                               objs_coord[max_two_conf_objs_id[1]])

        angle = YoloObj.CalcOrient(max_two_conf_objs, 
                                   max_two_conf_objs_id,
                                   temp_img.shape,
                                   two_temp_objs_coord)

        print('angle: ', angle)

    if len(objs) > 0:
        print('objs_coord: ', objs_coord, max_conf_obj_id, type(max_conf_obj_id))
        print('objs_coord[max_conf_obj_id]: ', objs_coord[max_conf_obj_id])

        xy_position_pixel, position_real = \
            YoloObj.PosMapping(max_conf_obj, 
                               img.shape, 
                               cam_fov_deg,
                               temp_realsize_mm,
                               temp_img.shape,
                               label_dict,
                               objs_coord[max_conf_obj_id])

        print('position: ', xy_position_pixel, position_real)

    # show information about camera position
    if len(objs) < 1:
        position_display = 'Unknown'
        position_str = 'Cam (X,Y,Z): {}'
    elif len(objs) > 0:
       position_display = str(tuple(map(int, list(position_real))))
       position_str = 'Cam (X,Y,Z): {} mm'

#    YoloObj.DrawBBox(objs, img)

    cv2.putText(img,
                position_str.format(position_display),
                (50, 50),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.9,
                (0, 0, 255),
                2,
                cv2.LINE_AA)

    cv2.circle(img, (int(img.shape[1]/2), int(img.shape[0]/2)), 15, (0, 0, 255), -1)

    # show informations about camera YAW
    if len(objs) < 2: 
        angle_display = 'Unknown'
        angle_str = '        YAW: {}'
    elif len(objs) > 1:
        angle_display = angle.copy()
        angle_str = '        YAW: {:.2f} degree'

    cv2.putText(img,
                angle_str.format(angle_display),
                (50, 90),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.9,
                (0, 0, 255),
                2,
                cv2.LINE_AA)


    if not noshow_img:
        YoloObj.ShowImg(img)

    if save_img:
        YoloObj.SaveImg(img, resize_ratio=float(args.resize))

    return objs, img


def VideoDetect(video_path, label_dict, 
                save_video=False, auto_label=False, skip_nolabel=False,
                resize=1.0, exclude_objs='background', autolabel_dir='images'):

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * float(resize))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * float(resize))
    print('fps:', fps)

    if save_video:
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

    ii=0
    while (cap.isOpened()):
        ii+=1
        ret, frame = cap.read()
        print('frame : ', ii, ret, type(frame))
        if not ret:
            break

#        frame = cv2.resize( frame, (int(frame.shape[1]*float(resize)), 
#                                    int(frame.shape[0]*float(resize))) )

        frame = cv2.resize(frame, (width, height))

        cv2.imwrite('tmp.jpg', frame)
 
        objs, img = ImgDetect('tmp.jpg', net, meta, darknet_data)

        new_objs = [obj for obj in objs if obj.name not in exclude_objs]
        for obj in new_objs:
            print('obj: ', obj.name, obj.conf)

        if auto_label:
            if not os.path.isdir(autolabel_dir): os.mkdir(autolabel_dir)
#            if not os.path.isdir('labels'): os.mkdir('labels')

            YoloObj.AutoLabeling(frame, new_objs, label_dict, 
                                 autolabel_dir + '/frame{:05d}.jpg'.format(ii),
                                 autolabel_dir + '/frame{:05d}.txt'.format(ii),
                                 skip_nolabel=args.skip_nolabel
                                )

#        img = YoloObj.DrawBBox(new_objs, frame, show=False, save=False)

        if save_video:
            out.write(img)

#        cv2.imshow(dirname + '/' + filename, img)
        cv2.imshow(args.video_path, img)

        k = cv2.waitKey(1) & 0xFF

        if k == 27 or k== ord('q'):
            break

    print('Prediction is finished.')

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if args.subparsers == 'video_detect':
        VideoDetect(args.video_path, label_dict, 
                    save_video=args.save_video,
                    auto_label=args.auto_label,
                    skip_nolabel=args.skip_nolabel,
                    resize=args.resize, 
                    exclude_objs=args.exclude_objs, 
                    autolabel_dir='images')

    elif args.subparsers == 'img_detect':
        ImgDetect(args.img_path, net, meta, darknet_data,
                  save_path='./test_pic.jpg', 
                  noshow_img=args.noshow_img, save_img=args.save_img)

    else:
        print('Nothing to do.')
