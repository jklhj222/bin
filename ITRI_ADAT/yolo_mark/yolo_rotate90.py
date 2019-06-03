#!/usr/bin/env python3

from PIL import Image

img_file = input("the image file name: ")
if '.jpg' in img_file: 
    filename = img_file.split(".jpg")[0]
elif '.png' in img_file: 
    filename = img_file.split(".png")[0]

img = Image.open(img_file)
width = img.size[0]
height = img.size[1]

print(img.size, width, height, img_file, filename)

#clockwise rotation
def rotate90(x, y, w, h):
    rot_x = 1 - y
    rot_y = x
    rot_w = h
    rot_h = w

    return (rot_x, rot_y, rot_w, rot_h)

with open(filename + ".txt", "r") as f:
    data = f.readlines()

#    print('data: ', data)
    if len(data) != 0:
        for datum in data:
            category = datum.split()[0]
            box_x = float(datum.split()[1])
            box_y = float(datum.split()[2])
            box_w = float(datum.split()[3])
            box_h = float(datum.split()[4])
#            print(category, box_x, box_y, box_w, box_h)
   
            box_rotate = rotate90(box_x, box_y, box_w, box_h)

#            print(box_rotate)
            with open("tmp.dat", "a") as f2:
                f2.write(category + " " + \
                         "{:.6f}".format(box_rotate[0]) + " " + \
                         "{:.6f}".format(box_rotate[1]) + " " + \
                         "{:.6f}".format(box_rotate[2]) + " " + \
                         "{:.6f}".format(box_rotate[3]) + '\n')
          
    elif len(data) == 0:
        with open('tmp.dat', 'w') as f2:
            f2.write('')





