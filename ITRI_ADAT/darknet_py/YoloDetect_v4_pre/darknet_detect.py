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

parser_video.add_argument('--check_delay',
                    help='time delay when checking. Default=33 ms (FPS: 30)',
                    default=33)

parser_video.add_argument('--save_video', default=False, action='store_true',
                          help='default=False')

parser_video.add_argument('--save_images', default=False, action='store_true',
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

darknet_model_dir = config['DARKNET']['MODEL_DIR']
files = sorted(os.listdir(darknet_model_dir), key=lambda x: x[::-1])
print(files)
for f in files:
    if f.endswith('.data'):
        darknet_data = os.path.join(darknet_model_dir, f)

    elif f.endswith('.weights'):
        darknet_weights = os.path.join(darknet_model_dir, f)

    elif f.endswith('.cfg'):
        darknet_cfg = os.path.join(darknet_model_dir, f)

    elif f.endswith('.names'):
        darknet_names = os.path.join(darknet_model_dir, f)

        with open(darknet_data, 'r') as ff:
            lines = ff.readlines()
 
        with open(darknet_data, 'w') as ff:
            for line in lines:
                if not line.startswith('names'):
                    ff.write(line)

            ff.write(f'names = {darknet_names}')

print(darknet_data, darknet_weights, darknet_cfg)

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

    results = DFUNC.detect(net, meta, bytes(img_path, encoding='utf-8'),
                           thresh=float(args.thresh))

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    for obj in objs:
        print(obj.obj_string, obj.cx, obj.cy)

    print('Number of objects: ', len(objs), '\n')

    YoloObj.DrawBBox(objs, img, 
                     show=not noshow_img, save=save_img, save_path=save_path)

    return objs


def VideoDetect(video_path, check_delay, label_dict, save_images=False,
                save_video=False, auto_label=False, skip_nolabel=False,
                resize=1.0, exclude_objs='background', autolabel_dir='images'):

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * float(resize))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * float(resize))
    print('test1: ', width, height)
    print('fps:', fps)

    if save_video:
        out = cv2.VideoWriter('output.avi', fourcc, 30.0, (width, height))

    ii=0

    if save_images:
        import shutil

        if not os.path.isdir('out_images'):
            os.mkdir('out_images')

        else:
            shutil.rmtree('out_images')

            os.mkdir('out_images')

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
 
        objs = ImgDetect('tmp.jpg', net, meta, darknet_data)

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

        img = YoloObj.DrawBBox(new_objs, frame, 
                               show=False, save=False,
                               line_width=1, text_size=3)

        if save_video:
            out.write(img)

        if save_images:
            cv2.imwrite(f'out_images/frame{ii:05d}.jpg', img)


#        cv2.imshow(dirname + '/' + filename, img)
        cv2.imshow(video_path, img)

        k = cv2.waitKey(int(check_delay)) & 0xFF

        if k == 27 or k== ord('q'):
            break

    print('Prediction is finished.')

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if args.subparsers == 'video_detect':
        print('check_delay: ', args.check_delay)
        VideoDetect(args.video_path, args.check_delay, label_dict,
                    save_images=args.save_images, 
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
