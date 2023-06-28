#!/usr/bin/env python3

from turtle import pos
import cv2
import time
import configparser
import argparse
import DarknetFunc as DFUNC
import YoloObj
import cv2
import os
import glob
import calc_period

parser = argparse.ArgumentParser()

# global parameters
parser.add_argument('--cfg_file', default='config.txt',
                    help='default="config.txt"')

parser.add_argument('--resize', default=1.0, help='default=1.0')

parser.add_argument('--gpu_idx', default='0', help='default=0')

parser.add_argument('--thresh', default=0.25, help='default=0.25')

parser.add_argument('--net_size', default=None, help='default=None')

parser.add_argument('--negative_obj', nargs='+', default='abnormal',
                         help='default="abnormal"')

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

parser_img.add_argument('--save_path', default='./test_pic.jpg', 
                        help='default=./test_pic.jpg')

parser_img.add_argument('--exclude_objs', nargs='+', default='background',
                        help='default="background"')

# parameters for images in a directory detection.
parser_imgs = subparsers.add_parser('imgs_detect', 
                                    help='single image detect.')
parser_imgs.add_argument('--imgs_path', default=None, 
                         required=True, help='default=None')

parser_imgs.add_argument('--noshow_img', default=False, 
                         action='store_true', help='default=True')

parser_imgs.add_argument('--save_img', default=False, 
                         action='store_true', help='default=False')

parser_imgs.add_argument('--target_class', default=None, 
                         help='positive class')

parser_imgs.add_argument('--output_dir', default=None, 
                         help='default=None')

parser_imgs.add_argument('--exclude_objs', nargs='+', default='background',
                         help='default="background"')

parser_imgs.add_argument('--auto_label', default=False, action='store_true',
                         help='default=False')

parser_imgs.add_argument('--skip_nolabel', default=False, action='store_true',
                          help='default=False')

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

if args.net_size is not None:
    YoloObj.ChangeNetSize(darknet_cfg, args.net_size)

net = DFUNC.load_net(bytes(darknet_cfg, 'utf-8'), 
                     bytes(darknet_weights, 'utf-8'), 0)
meta = DFUNC.load_meta(bytes(darknet_data, 'utf-8'))

#filename = os.path.basename(args.video_path)
#dirname = os.path.basename(os.path.dirname(args.video_path))

label_dict = {}
for idx in range(meta.classes):
    label_dict[meta.names[idx]] = idx

label_count_dict = {}
for label_count in label_dict:
    label_count_dict[label_count.decode()] = 0

print('label_dict: ', label_dict)
print('label_count_dict: ', label_count_dict)

def ImgDetect(img_path, net, meta, darknet_data, save_path='./',
              noshow_img=True, negative_obj=[], save_img=False):

    import YoloObj

    img = cv2.imread(img_path)

    results = DFUNC.detect(net, meta, bytes(img_path, encoding='utf-8'),
                           thresh=float(args.thresh))

    objs = []
    for result in results:
        obj = YoloObj.DetectedObj(result)
        objs.append(obj)

    # print info.
    print(args.imgs_path)
    for obj in objs:
        print(obj.obj_string, obj.cx, obj.cy) 
    print(f'Number of objects: {len(objs)},  target_class: {args.target_class}')

    YoloObj.DrawBBox(objs, img, show=not noshow_img, 
                     save=save_img, negative_obj=negative_obj, save_path=save_path)

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
                  save_path=args.save_path, 
                  noshow_img=args.noshow_img, save_img=args.save_img)

    elif args.subparsers == 'imgs_detect':
        img_fs = glob.glob(os.path.join(args.imgs_path, '*.jpg')) 
        img_fs.extend(glob.glob(os.path.join(args.imgs_path, '*.png')))
        img_fs.sort()
        total_frame = len(img_fs)

        output_dir = args.output_dir
        result_log = output_dir + '_log.txt' 
        f_log = open(result_log, 'w')

        if args.target_class:
            positive_confs = []
            negative_confs = []
 
        time_period = calc_period.TimePeriod()
        frame_detected = 0
        nobj = 0
        for idx, img_f in enumerate(img_fs):
            t = time_period.calc_period()

            img_f_basename = os.path.basename(img_f)
     
            save_path = os.path.join(output_dir, img_f_basename)

            objs = ImgDetect(img_f, net, meta, darknet_data,
                             save_path=save_path, negative_obj=args.negative_obj,
                             noshow_img=args.noshow_img, save_img=args.save_img)

            exclude_objs = args.exclude_objs
            new_objs = [obj for obj in objs if obj.name not in exclude_objs]

            if args.auto_label:
                frame = cv2.imread(img_f)
                label_output_dir = os.path.join(output_dir, 'label', output_dir)
                os.makedirs(label_output_dir, exist_ok=True)  

                img_path = os.path.join(label_output_dir, img_f_basename)
                label_path = os.path.join(label_output_dir, img_f_basename.split('.')[0] + '.txt')
                YoloObj.AutoLabeling(frame, new_objs, label_dict,
                                    img_path, label_path, skip_nolabel=args.skip_nolabel)


            f_log.write(str(idx+1) + ': ' + img_f + '\n')
            if args.target_class and len(objs) == 0:
                print(f'Empty, Frame detected: {frame_detected}, Total: {idx+1}/{total_frame}')
      
            if not args.target_class:
                print(f'Frame detected: {frame_detected}, Total: {idx+1}/{total_frame}')

            if len(objs) != 0:
                nobj += len(objs)
                frame_detected += 1

            for obj in objs:
                label_count_dict[obj.name] += 1

                if args.target_class:
                    if obj.name == args.target_class:
                        positive_confs.append(obj.conf)
                        f_log.write(f'{obj.obj_string}   True\n')
                        print(f' True, Frame detected: {frame_detected}, Total: {idx+1}/{total_frame}')
                    else:
                        negative_confs.append(obj.conf)
                        f_log.write(f'{obj.obj_string}   False\n')
                        print(f'False, Frame detected: {frame_detected}, Total: {idx+1}/{total_frame}')


            f_log.write('\n')
            print(f'{t}\n')

        if args.target_class:
            positive_confs.sort()
            negative_confs.sort()
            total_tag = len(positive_confs) + len(negative_confs)

        f_log.write(str(darknet_model_dir) + '\n')
        f_log.write(str(label_count_dict) + '\n')

        if args.target_class:
            if total_tag > 0:
                accuracy = label_count_dict[args.target_class] / total_tag * 100
                anti_acc = 100 - accuracy
                acc_str_f = '{:.1f}'
            else:
                accuracy = 'N/A'
                anti_acc = 'N/A'
                acc_str_f = '{:s}'

            recall_str_f = '{:.1f}'
            recall = (len(positive_confs)/total_frame) * 100

            f_log.write(f'    target class: {args.target_class}\n')
            f_log.write(f'    Total frames: {total_frame:6d}\n')
            f_log.write(f'    Empty frames: {total_frame-frame_detected:6d}\n')
            f_log.write(f'      Total tags: {nobj:6d}\n')
            f_log.write(f'   True Positive: {len(positive_confs):6d}\n')
            f_log.write(f'  False Negative: {len(negative_confs):6d}\n')
            f_log.write(f'        Accuracy: {accuracy:6.1f}\n') if acc_str_f == '{:.1f}' else f_log.write(f'        Accuracy: {accuracy:>6s}\n')
            f_log.write(f'          Recall: {recall:6.1f}\n')
 
            if len(positive_confs) > 0:
                positive_conf = sum(positive_confs)/len(positive_confs)
                pos_min_conf = positive_confs[0]
                pos_max_conf = positive_confs[-1]
                pos_str_f = '{:.1f}'
                f_log.write(f'   Positive conf: {positive_conf:>6.1f} {pos_min_conf:>6.1f} {pos_max_conf:>6.1f}\n')
            else:
                positive_conf = pos_min_conf = pos_max_conf = 'N/A'
                pos_str_f = '{:s}'
                f_log.write(f'   Positive conf: {"N/A":>6s} {"N/A":>6s} {"N/A":>6s}\n')

            if len(negative_confs) > 0:
                negative_conf = sum(negative_confs)/len(negative_confs)
                neg_min_conf = negative_confs[0]
                neg_max_conf = negative_confs[-1]
                neg_str_f = '{:.1f}'
                f_log.write(f'   Negetive conf: {negative_conf:>6.1f} {neg_min_conf:>6.1f} {neg_max_conf:>6.1f}\n')
            else:
                negative_conf = neg_min_conf = neg_max_conf = 'N/A'
                neg_str_f = '{:s}'
                f_log.write(f'   Negetive conf: {"N/A":>6s} {"N/A":>6s} {"N/A":>6s}\n')

            target_str = ''
            target_str_f = ''
            target_num = []
            for target in label_count_dict:
                target_str += ',' + target
                target_str_f += ',{}'
                target_num.append(label_count_dict[target])

            summary_title = 'clip,total_frame,empty_frame,' \
                            + 'accuracy,recall,' \
                            + 'acc_avg_conf,acc_min_conf,acc_max_conf,' \
                            + 'false_rate,' \
                            + 'false_avg_conf,false_min_conf,false_max_conf' \
                            + target_str \
                            + '\n'
            summary_str_f = '{},{},{},' \
                            + acc_str_f + ',' + recall_str_f + ',' \
                            + pos_str_f + ',' + pos_str_f + ','+ pos_str_f + ',' \
                            + acc_str_f + ',' \
                            + neg_str_f + ',' + neg_str_f + ',' + neg_str_f  \
                            + target_str_f \
                            + '\n'

            imgs_dir_base = os.path.basename(args.imgs_path)
            summary_str = summary_str_f.format(imgs_dir_base, total_frame, total_frame-frame_detected,
                                               accuracy, recall, 
                                               positive_conf, pos_min_conf, pos_max_conf, 
                                               anti_acc, 
                                               negative_conf, neg_min_conf, neg_max_conf,
                                               *target_num)

            f_log.write(f'Models: {darknet_model_dir}\n')
            f_log.write(summary_title)
            f_log.write(summary_str)

        else:
            f_log.write(f'    Total frames: {total_frame:6d}\n')
            f_log.write(f' Detected frames: {frame_detected:6d}\n')
            f_log.write(f'      Total tags: {nobj:6d}\n')
            f_log.write(f'Models: {darknet_model_dir}\n')

        f_log.close()

    else:
        print('Nothing to do.')
