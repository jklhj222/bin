import numpy as np
import cv2
from glob import glob
import os
from sys import argv

if len(argv) == 1:
    print("$1 is dataset name or part of it")
    quit()

dirname = argv[1].strip("/")
dirnames = glob(dirname+"*")
if len(dirnames) == 0:
    print("no datasets with name \"%s\" are found"%dirname)
    quit()
elif len(dirnames) == 1:
    dataset_input = dirnames[0]
else:
    if argv[1] in dirnames:
        dataset_input = dirname
    else:
      print("more than one dataset with name \"%s\" are found"%dirname)
      quit()
dir_image = dataset_input+"/images/"
dir_label = dataset_input+"/labels/"

time_interval = 1
labeled_only  = 0
save_video    = 0

image_names = sorted(glob(dir_image+"/*"))
print("# of images: %d"%len(image_names))

if save_video:
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  height_image, width_image = cv2.imread(image_names[0]).shape[:2]
  output = cv2.VideoWriter('output.avi',fourcc, 50.0, (width_image,height_image))

def yolo_xymm(bbox_yolo,height_image,width_image):
  bbox_yolo = bbox_yolo.strip("\n").split()
  category      =   int(bbox_yolo[0])
  x_center_bbox = float(bbox_yolo[1])
  y_center_bbox = float(bbox_yolo[2])
  width_bbox    = float(bbox_yolo[3])
  height_bbox   = float(bbox_yolo[4])
  x_left   = int( (x_center_bbox- width_bbox/2.) * width_image )
  x_right  = int( (x_center_bbox+ width_bbox/2.) * width_image )
  y_top    = int( (y_center_bbox-height_bbox/2.) * height_image )
  y_bottom = int( (y_center_bbox+height_bbox/2.) * height_image )
  return category, x_left, y_top, x_right, y_bottom

colors = [(250,250,250),(5,250,250),(250,5,250),(250,250,5),(10,100,200),(20,80,130),(30,60,210)]

forward = True
count = 0
#for count,image_name in enumerate(image_names):
key = ''
while key != ord('q'):

  image_name = image_names[count]
  print(image_name)
  label_name = dir_label+"/"+os.path.splitext(os.path.basename(image_name))[0]+".txt"
  with open(label_name) as f:
    labels = f.readlines()

  if len(labels) == 0 and labeled_only:
    continue
  else:
    image = cv2.imread(image_name)
    height_image, width_image = image.shape[:2]

  for bbox_yolo in labels:
    category, x_left, y_top, x_right, y_bottom = yolo_xymm(bbox_yolo,height_image,width_image)
    cv2.rectangle(image,(x_left-1,y_top-1),(x_right+1,y_bottom+1),(  5,  5,  5),2)
    cv2.rectangle(image,(x_left  ,y_top  ),(x_right  ,y_bottom  ),colors[category],2)
  image = cv2.putText(image,"%06d"%count,(102,102),cv2.FONT_HERSHEY_TRIPLEX, 1, (  5,   5,   5), 1, cv2.LINE_AA)
  image = cv2.putText(image,"%06d"%count,(100,100),cv2.FONT_HERSHEY_TRIPLEX, 1, (250, 250, 250), 1, cv2.LINE_AA)

  cv2.imshow("test",image)
  if save_video:
    output.write(image)

  if count==0 and key!='':
    key = cv2.waitKey(0)
  else:
    key = cv2.waitKey(time_interval)

  if key == ord('s'):
    key = cv2.waitKey(0)
  if key == ord('d'):
    forward = True
  if key == ord('a'):
    forward = False

  count += 1 if forward else -1
  while count<0:
    count += len(image_names)
  while count>=len(image_names):
    count -= len(image_names)
