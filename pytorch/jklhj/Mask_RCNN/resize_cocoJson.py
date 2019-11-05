#!/usr/bin/env python3

import json

origin_file = 'trainval.json'
resized_file = 'trainval_resize0.2.json'

# (height, width)
origin_size = (3288, 4608)
resized_size = (658, 922)

resize_ratio = (resized_size[0]/origin_size[0], 
                resized_size[1]/origin_size[1])
print(resize_ratio)

with open(origin_file, 'r') as f:
    json_str = f.read()

j = json.loads(json_str)

def resize_SegBox(i, x):
    if i%2==0:
        return x * resize_ratio[0]

    else:
        return x * resize_ratio[1]

# change picture size
for i in range(len(j['images'])):
    j['images'][i]['height'] = resized_size[0]
    j['images'][i]['width'] = resized_size[1]

for i in range(len(j['annotations'])):
    # resize the segmentation
    resized_seg = list(map(resize_SegBox,
                           [idx for idx in range(len(j['annotations'][i]['segmentation'][0]))],
                           j['annotations'][i]['segmentation'][0]) 
                      )
    j['annotations'][i]['segmentation'][0] = resized_seg

    # resize the area
    resized_area = j['annotations'][i]['area'] * resize_ratio[0] * resize_ratio[1]
    j['annotations'][i]['area'] = resized_area

    # resize the bbox
    resized_box = list(map(resize_SegBox,
                           [idx for idx in range(len(j['annotations'][i]['bbox']))],
                           j['annotations'][i]['bbox']))
    j['annotations'][i]['bbox'] = list(map(lambda x: float('{:.1f}'.format(int(x))), 
                                       resized_box))


print(j)

jsObj = json.dumps(j, indent=3)
print(jsObj)

with open(resized_file, 'w') as f:
    f.write(jsObj)

