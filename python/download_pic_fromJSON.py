#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 20:15:36 2018  jklhj
"""

import json
import requests

JSON_FILE = 'test.json'

file = open(JSON_FILE, 'r').read()
jfile = json.loads(file)

#print(len(jfile['images']))
#print(jfile['images'][0])
#print(len(jfile['images'][0]))

imageID_url = [ (i['imageId'], i['url']) for i in jfile['images'] ]
print('lengh of imageID_url: ', len(imageID_url))

for i, j in imageID_url:
    print(i,j)
    r = requests.get(j)
    with open('./test_pic/' + '{:06d}'.format(i), 'wb') as f:
        f.write(r.content)





