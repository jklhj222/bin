import cv2
from commands import getoutput as gop
from sys import argv
from os.path import isfile
import time

def getFilename(keyword):
  with open('config.txt') as f:
    for datum in f.readlines():
      datum = datum.strip('\n').split('=')
      if datum[0] == keyword:
        return datum[1]
  print('Cannot get filename of example video from config.txt')
  quit()
  return
#filename = '/home/adat/Error3_60cm_away_165cm_height.MTS'
filename = getFilename("path_example")

if not isfile(filename):
  print('check file')
  quit()
dirname  = filename.split('/')[-1].split('.')[0]
#dirname = '/home/adat/results/'
#dirname = '../data/'
dirname = getFilename("path_data")
print(filename, dirname)

gop('mkdir -p '+dirname)
vidcap = cv2.VideoCapture(filename)
success, image = vidcap.read()
count = 0
while success:
  time.sleep(0.05)
  cv2.imwrite(dirname+"/images/res_%08d.jpg"%count, image)
  success, image = vidcap.read()
  if not success:
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
  image = cv2.flip(image,0)
  print(count)
  count += 1

