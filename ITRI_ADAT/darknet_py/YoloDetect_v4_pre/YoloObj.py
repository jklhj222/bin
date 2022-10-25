#!/usr/bin/env python3
""" Created on Wed Jan 23 16:03:43 2019 @author: jklhj """
from math import ceil, sqrt
import sys 
import cv2 

class DetectedObj():
    def __init__(self, result):
        self.name = result[0].decode('utf-8')
        self.conf = int(round(result[1]*100))
        self.bbox_yolo = result[2]

        self.bbox = self.calc_bbox(result[2][0],
                                   result[2][1],
                                   result[2][2],
                                   result[2][3])

        self.cx = int(result[2][0])
        self.cy = int(result[2][1])
        self.l = self.bbox[0]
        self.r = self.bbox[1]
        self.t = self.bbox[2]
        self.b = self.bbox[3]
        self.w = self.bbox[4]
        self.h = self.bbox[5]
        self.a = self.bbox[6]

        self.obj_string = '{"' + self.name + \
                          '":' + str(self.conf) + \
                          ',"left":'  + str(self.l) + \
                          ',"right":' + str(self.r) + \
                          ',"top":'   + str(self.t) + \
                          ',"bot":'   + str(self.b) + '}'
   
 
    def calc_bbox(self, x, y, w, h):
        left   = int(x - w/2)
        right  = int(x + w/2)
        top    = int(y - h/2)
        bottom = int(y + h/2)
        width  = right - left
        height = bottom - top
        area   = width * height
        
        return (left, right, top, bottom, width, height, area)

    def CalcInOutObj(inout_pairs, poi_thresh, objs):
        all_POIs = []
        all_innerObjs = []
#        out = []
        OutObjs = []
        for innerName, outerName in inout_pairs:
            if innerName == outerName:
                print('\nThe inner object and outer object are the same, '
                      'are you serious? '
                      'Check the config.txt again, OK?')
             
                sys.exit()

            innerObjs = [obj for obj in objs if obj.name == innerName]
            outerObjs = [obj for obj in objs if obj.name == outerName]
            print('innerObjs: ', innerObjs, len(innerObjs))
            print('outerObjs: ', outerObjs, len(outerObjs))

            num_outer = len(outerObjs)
    
            POIs = [ ObjsPOI(inner, outer) 
                       for inner in innerObjs
                       for outer in outerObjs ]
    
            all_POIs.append( (num_outer, POIs) )
            all_innerObjs.append(innerObjs)
    
        print('all_POIs:', all_POIs)
        for idx_pair, pair in enumerate(all_POIs):
            print('pair:', pair)
            print('pair[1]: ', pair[1], len(pair[1]))
            for idx_POI, POI in enumerate(pair[1]):
                print('idx_POI, POI, poi_thresh:', idx_POI, POI, poi_thresh)
                if POI >= poi_thresh and pair[0] > 0.0:
                    idx_inner = ceil((idx_POI+1) / pair[0]) - 1
                    print('idx_inner, pair[0]:', idx_inner, pair[0])
                    
                    print(all_innerObjs[idx_pair][idx_inner].name)
                    obj = all_innerObjs[idx_pair][idx_inner]
    
                    OutObjs.append(obj)
                    
        return OutObjs
    
#                    out_string = WriteToFile(obj, img_file).string
#                    out.append(out_string)
#                    WriteToFile.ToFile(out, 
#                                       path.join(data_dir, 
#                                                 config['DATA']['RES_FILE']) )
                    
                    
def WriteToFile(img_file, out_file, objs):
    if len(objs) != 0:
        obj_string = ','.join([obj.obj_string for obj in objs])
        out_string = '{"filename":"' + img_file + \
                          '","tag":[' + obj_string + ']}'

    else:
        out_string = '{"filename":"' + img_file + '","tag":[]}'

    print(out_file)
    with open(out_file, 'a') as f:
        f.write(out_string + '\n')


def ObjsPOI(innerObj, outerObj):
    w_POI = (outerObj.w + innerObj.w) \
            - ( max(innerObj.l, innerObj.r, outerObj.l, outerObj.r) 
               -min(innerObj.l, innerObj.r, outerObj.l, outerObj.r) )
    
    h_POI = (outerObj.h + innerObj.h) \
            - ( max(innerObj.t, innerObj.b, outerObj.t, outerObj.b) 
               -min(innerObj.t, innerObj.b, outerObj.t, outerObj.b) )
            
    POI = (w_POI * h_POI)*1.0 / innerObj.a if w_POI > 0 and h_POI > 0 else 0.0
    
    return POI 


def DrawBBox(objs, img, show=True, save=False, 
             line_width=1, text_size=3, negative_obj=[],
             save_path='./test_pic.jpg', resize_ratio=None):
#    import cv2

    for obj in objs:
        if obj.name in negative_obj:
            color = (0, 0, 255)

        else:
            color = (0, 255, 0)

        cv2.rectangle(img, (obj.l, obj.t), (obj.r, obj.b), color, text_size)

        text_x = obj.l
        text_y = obj.t - 10 if obj.t > 30 else obj.b + 20 
        image = cv2.putText(img,
                            obj.name + ':' + str(obj.conf),
                            (text_x, text_y), 
                            cv2.FONT_HERSHEY_TRIPLEX, 
                            0.5, 
                            color, 
                            line_width, 
                            cv2.LINE_AA)

    if resize_ratio is not None:
        width   = int(img.shape[0] * resize_ratio)
        height  = int(img.shape[1] * resize_ratio)

        img = cv2.resize(img, (height, width))

    if save == True: 
        cv2.imwrite(save_path, img)

    if show == True:
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return img


def AutoLabeling(img, objs, label_dict, 
                 img_path, label_path, skip_nolabel=False):
    # label_dict: {b'object1': 0, b'object2': 1, ...}
    # skip_nolabel == True : don't generate labels and images which detect nothing

    if len(objs) == 0 and skip_nolabel:
        print('skip no label.')
        pass

    else:
        height, width, channel = img.shape    
        
        with open(label_path, 'w') as f:
            if len(objs) == 0:
                cv2.imwrite(img_path, img)
        
            else:
                for obj in objs:
                    cx = obj.cx / width
                    cy = obj.cy / height
        
                    w = obj.w / width
                    h = obj.h / height
        
                    cv2.imwrite(img_path, img)
        
                    idx = label_dict[bytes(obj.name, encoding='utf8')]
 
                    f.write('{} {} {} {} {}'.format(idx, cx, cy, w, h))


# direction = "right" or "left"
def ObjFlowNum(cur_objs, pre_objs, direction, baseline):
    direction = 1 if direction=="right" else -1

    obj_pairs = []
    for cur_obj in cur_objs:
        dists = []
        for pre_obj in pre_objs:
            dist = sqrt( (cur_obj.cx - pre_obj.cx)**2 + 
                              (cur_obj.cy - pre_obj.cy)**2 )

            dists.append(dist)

        obj_pairs.append( (cur_obj, pre_objs[ dists.index(min(dists)) ]) )

    print('obj_pairs: ', len(obj_pairs), baseline)
    num_obj = 0
    for obj_pair in obj_pairs:
        print('obj_pair[0].cx: ', obj_pair[0].cx, obj_pair[1].cx)
        if (obj_pair[0].cx - baseline) * direction > 0 and \
                          (baseline - obj_pair[1].cx) * direction > 0:
            num_obj += 1

    return num_obj


def ChangeNetSize(darknet_cfg, net_size):
    with open(darknet_cfg, 'r') as f:
        lines = f.readlines()

    with open(darknet_cfg, 'w') as f_w:
        for line in lines:
            if 'width' in line:
                line = line.replace(line, f'width = {net_size}\n')
            if 'height' in line:
                line = line.replace(line, f'height = {net_size}\n')

            f_w.write(line)



