#!/usr/bin/env python3
""" Created on Wed Sep 26 14:03:10 2018 @author: jklhj """

import argparse
import getpass
import os
import sys
from subprocess import call
import cv2
import shutil
import xml.etree.ElementTree as ET
from glob import glob

NAME_CONTAINER = 'vatic00'
DIRNAME_VATIC = 'data_vatic'
LABEL_LIST = 'labels.txt'
USER_NAME = getpass.getuser()
print(USER_NAME)

# set arguments
parser = argparse.ArgumentParser(
        description='For labeling tool "vatic". ')

parser.add_argument('--video_path',
                    default='',
                    help='the video file to split into frames.')

parser.add_argument('--image_quality',
                    default=80,
                    help='the quality of output images. Default=80')

parser.add_argument('--check_labels',
                    help='set to check the results after splitting the video.'
                         ' Default=False',
                    default=False,
                    action='store_true')

parser.add_argument('--check_delay',
                    help='time delay when checking. Default=1 ms',
                    default=1)

parser.add_argument('--check_labels_only',
                    help='set to check the results only. Default=False',
                    default=False,
                    action='store_true')

parser.add_argument('--vatic_only',
                    help='set to open vatic docker only. Default=False',
                    default=False,
                    action='store_true')

parser.add_argument('--show_images_with_no_labels',
                    help='set to show the images without any labels. Default=False',
                    default=False,
                    action='store_true')

args = parser.parse_args()

if not args.video_path: 
    print('Error: Need to set the path of video file: --video_path')
    sys.exit()

#check the files we need
if not os.path.isfile(args.video_path): 
    print("the video file", args.video_path, "doesn't exist.")
    sys.exit()
else: 
    print(args.video_path)

if not os.path.isfile(LABEL_LIST) and not args.check_labels_only:
    print("the label list file", LABEL_LIST, "doesn't exist. "
          "One line for one class name.")
    sys.exit()
else:
    print(LABEL_LIST)
    
video_basename = os.path.basename(args.video_path)
data_dir = 'data_' + os.path.splitext(video_basename)[0]
images_dir = 'data_' + os.path.splitext(video_basename)[0] + '/images'

# remove old data directory
if os.path.exists('data_vatic') and not args.vatic_only: 
    yes_no = input('data_vatic directory already exists, remove it? (y/n) :\n')
    if yes_no == 'y':
        call(['sudo', 'rm', '-r', 'data_vatic'])

if not os.path.exists( images_dir ):
    os.makedirs( images_dir )

def cut_video_to_frames(video=args.video_path, 
                        frames_dir=images_dir,
                        quality=args.image_quality):
    vc = cv2.VideoCapture(video)
    
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
        
    vc.release() 
    vc = cv2.VideoCapture(video)
    
    c = 0
    while rval:
        print('frame: ', c)
        rval, frame = vc.read()                
        if rval:
            file_name = os.path.join(frames_dir, 
                                     'frame' + '{:05d}.jpg'.format(c))
            cv2.imwrite(file_name, 
                        frame, 
                        [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
        c += 1
    vc.release()        
        
    
def exc_vatic_docker(video=args.video_path):
    if not os.path.exists('data_vatic/videos_in'): 
        os.makedirs('data_vatic/videos_in')

    shutil.copy(args.video_path, 'data_vatic/videos_in/')
    shutil.copy(LABEL_LIST, 'data_vatic/')
    shutil.copy(LABEL_LIST, data_dir + '/')
    
    print('------------------------- Reminder ----------------------------\n\n'
          'Now we are going to start vatic_docker, '
          'the superuser permission is needed.\n'
          'If the container', NAME_CONTAINER, 'already exists, remove it.\n'
          'Open browser with localhost:8111/directory .\n'
          'After finishing vatic, key in "exit" to leave the container.\n\n'
          '----------------------------------------------------------------\n')

    stop = input('Video split finished, press Enter to start vatic_docker, '
                 'have to enter the sudo password. '
                 'Then open browser with localhost:8111/directory .')
    
    if stop == '':
        if args.vatic_only:
            call(['chmod', 'a+w', os.getcwd() + '/data_vatic/output.xml'])

        docker_command = ['sudo', 'docker', 'run', '-it', '--name',
                          NAME_CONTAINER, '-p', '8111:80', '-v',
                          os.getcwd() + '/data_vatic:/root/vatic/data',
                          'npsvisionlab/vatic-docker', '/bin/bash', '-C',
                          '/root/vatic/example.sh']

        call(docker_command)
   
    
def vaticXMLtoYOLO(data_dir=data_dir):
    xml_name = 'data_vatic/output.xml'

    # make labels directory
#    if not os.path.exists(data_dir + '/labels'):
#        os.makedirs(data_dir + '/labels')

    # check the resolution in vatic
    height, width = cv2.imread('data_vatic/frames_in/0/0/0.jpg').shape[0:2]
    
    # check the resolution in original video
    height0, width0 = cv2.imread( data_dir + 
                                 '/images/frame' + 
                                 '{:05d}.jpg'.format(1) ).shape[0:2]

    tree = ET.parse(xml_name)
    root = tree.getroot()
    
    with open('labels.txt') as f:
        label_list = [ label.strip('\n') for label in f.readlines() ]

    for child1 in root.getchildren():
        first = True
        if child1.tag == 'object':
            
            for child2 in child1.getchildren():
                for i, label in enumerate(label_list):
                    if child2.text == label:
                        index_class = i
                        
                if child2.tag == 'polygon':
                    frame_number = int(child2[0].text)
                    if first:
                        ignore = frame_number + 300
                        first = False
                    if frame_number > ignore:
                        break
                    
                    x1 = int(int(child2[1][0].text)*width0/width)
                    y1 = int(int(child2[1][1].text)*height0/height)
                    x2 = int(int(child2[3][0].text)*width0/width)
                    y2 = int(int(child2[3][1].text)*height0/height)

                    image_name = data_dir + \
                                 '/images/frame{:05d}.jpg'.format(frame_number)
#                    label_file = data_dir + \
#                                 '/labels/frame{:05d}.txt'.format(frame_number)
                    label_file = data_dir + \
                                 '/images/frame{:05d}.txt'.format(frame_number)
                                 
                    if not os.path.isfile(image_name):
                        print("the image {} doesn't exist.".format(image_name))
                        sys.exit()
                 
                    # to show the images with bounding box
                    if args.check_labels:
                        image = cv2.imread(image_name)
                        print(image_name)
                        print(x1, y1, x2, y2, width0, width, height0, height)
                        
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,255), 5)
                        cv2.imshow('Image', 
                                   cv2.resize(image, 
                                              (int(width0*0.6),
                                               int(height0*0.6))))
                        
                        cv2.waitKey(1)
                        
                    xc = (x1 + x2)/2.0/width0
                    yc = (y1 + y2)/2.0/height0
                    xw = abs(x2 - x1)*1.0/width0
                    yh = abs(y2 - y1)*1.0/height0
                    
                    print(xc, yc, xw, yh)
                    with open(label_file, 'a') as f:
                        f.write( str(index_class) + ' ' +
                                 str(xc) + ' ' +
                                 str(yc) + ' ' +
                                 str(xw) + ' ' +
                                 str(yh) + ' \n' )
    
    # touch the files that without bounding boxes
    imagenames = glob(data_dir + '/images/*.jpg')
    
    textnames = []
    for imagename in imagenames:
        filename = imagename.strip('.jpg').split('/')[-1]
        
        textname = filename + '.txt'
#        textnames.append( data_dir + '/labels/' + textname)
        textnames.append( data_dir + '/images/' + textname)
        
#        call(['touch', data_dir + '/labels/' + textname])
        call(['touch', data_dir + '/images/' + textname])

    shutil.copy('data_vatic/output.xml', data_dir + '/')

    call(['sudo', 'chown', '-R', USER_NAME + ':' + USER_NAME,
          data_dir, 'data_vatic'])


def yolo_xymm(bbox_yolo):#,size):
  #height_image,width_image = size
  category      =       bbox_yolo[0]
  x_center_bbox = float(bbox_yolo[1])
  y_center_bbox = float(bbox_yolo[2])
  width_bbox    = float(bbox_yolo[3])
  height_bbox   = float(bbox_yolo[4])
  #x_left   = int( (x_center_bbox- width_bbox/2.) * width_image )
  #x_right  = int( (x_center_bbox+ width_bbox/2.) * width_image )
  #y_top    = int( (y_center_bbox-height_bbox/2.) * height_image )
  #y_bottom = int( (y_center_bbox+height_bbox/2.) * height_image )
  x_left   = x_center_bbox -  width_bbox/2.
  x_right  = x_center_bbox +  width_bbox/2.
  y_top    = y_center_bbox - height_bbox/2.
  y_bottom = y_center_bbox + height_bbox/2.
  return [category, x_left, y_top, x_right, y_bottom]


def check_labels(data_dir=data_dir):
    # check consistency
#    txt_list = glob(data_dir + '/labels/*.txt')
    txt_list = glob(data_dir + '/images/*.txt')
    img_list = glob(data_dir + '/images/*.jpg')
    print(len(txt_list), len(img_list))
    txt_list.sort()
    img_list.sort()
    
    if len(txt_list) != len(img_list):
        print('# of images and labels are not the same.')
        sys.exit()

    zipped = list(zip(txt_list, img_list))
    for i, j in enumerate(zipped):
        txt_path, img_path = j
        if txt_path.split('/')[-1][:-4] != img_path.split('/')[-1][:-4]:
            print(txt_path + ' ' + img_path + ' are not the same.')
            sys.exit()

    # show the images with bounding boxes
    time_interval = int(args.check_delay)
    allshow = 0
    
    for i, j in enumerate(zipped):
        txt_path, img_path = j
        labeled = False if not args.show_images_with_no_labels else True
        labels_list = []
        
        with open(txt_path) as f:
            for txt in f.readlines():
                labeled = True
                txt = txt.strip('\n')
                bbox_yolo = txt.split()
                label = yolo_xymm(bbox_yolo)
                labels_list.append(label)
    
        if allshow or labeled:
            img = cv2.imread(img_path)
            img_height, img_width = img.shape[0:2]
            
            for label in labels_list:
                category, xmin, ymin, xmax, ymax = label
                
                xmin = int( xmin*img_width )
                xmax = int( xmax*img_width )
                ymin = int( ymin*img_height )
                ymax = int( ymax*img_height )

                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 5)
                cv2.line(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 5)
                cv2.line(img, (xmax, ymin), (xmin, ymax), (0, 0, 255), 5)
                cv2.circle(img, (int((xmax+xmin)/2.0), int((ymax+ymin)/2.0)), 15, (0, 255, 0), -1)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, category, (xmin, ymin), font, 
                            1, (255, 255, 255), 2, cv2.LINE_AA)
            
            print('{:d}/{:d}'.format(i, len(zipped)),  img_width, img_height)

            
            cv2.imshow('Image', 
                       cv2.resize(img, 
                                  (int(img_width*0.6), int(img_height*0.6))))
            
            if cv2.waitKey(time_interval) & 0xff == ord('q'):
                break
    

if __name__ == '__main__':
    if not args.check_labels_only and not args.vatic_only:
        cut_video_to_frames(video=args.video_path,
                            frames_dir=images_dir,
                            quality=args.image_quality)
        
        exc_vatic_docker(video=args.video_path)
        
        call(['sudo', 'docker', 'rm', NAME_CONTAINER])
        
        vaticXMLtoYOLO(data_dir=data_dir)

    elif args.check_labels_only and not args.vatic_only: 
        check_labels(data_dir)

    elif args.vatic_only:
        exc_vatic_docker(video=args.video_path)
        
        call(['sudo', 'docker', 'rm', NAME_CONTAINER])
        
        vaticXMLtoYOLO(data_dir=data_dir)
        
    print('\nProgram finished.')
