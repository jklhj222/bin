#!/usr/bin/env python3
import numpy as np
import cv2


def findObjects(outputs, img):
    hT, wT, cT = img.shape
    print('img.shape: ', img.shape)
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
#            print('det: ', det)
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > 0.3:
                w, h = int( det[2]*wT ), int(det[3]*hT)
                x, y = int(det[0]*wT-w/2), int(det[1]*hT-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, 0.5, 0.3)
    return indices, bbox, classIds, confs


def AI_detect():
    cut_x = (200)
    whT = 416

    classesFile = './yolo/coco.names'
    classNames = []

    with open(classesFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    modelConfiguration = './yolo/yolov3-tiny.cfg'
    modelWeights = './yolo/yolov3-tiny.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#    img = MC_user.get_img()
    img = cv2.imread('test2.jpg')
    h, w, c = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], 1, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [ layerNames[i[0]-1] for i in net.getUnconnectedOutLayers() ]
    outputs = net.forward(outputNames)
  

    indices, bbox, classIds, confs = findObjects(outputs, img)
#    img = cv2.resize(img, (whT, whT))

    return img, indices, bbox, classIds, confs

if __name__ == '__main__':
    img, indices, bbox, classIds, confs = AI_detect()
    
    for i in range(len(bbox)): 
        (x, y, w, h) = bbox[i]

        cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 255), 5)
        cv2.circle(img, (int((x+w/2)), int((y+h/2))), 5, (255, 0, 255), -1)
        cv2.putText(img, str(i), (int((x+w/2)), int((y+h/2))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

    cv2.imwrite('test.jpg', img)

    print(f'indices:{indices}\n bbox:{bbox}\n classIds:{classIds}\n confs:{confs}')

