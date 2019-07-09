#!/usr/bin/env python3

import dlib
import numpy as np
import cv2
import os
import json

detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

imagePath = './'                                                                                    #影象的目錄
data = np.zeros((1,128))                                                                            #定義一個128維的空向量data
label = []                                                                                          #定義空的list存放人臉的標籤

for file in os.listdir(imagePath):                                                                  #開始一張一張索引目錄中的影象
    if '.jpg' in file or '.png' in file:
        fileName = file
        labelName = file.split('_')[0]                                                              #獲取標籤名
        print('current image: ', file)
        print('current label: ', labelName)
        
        img = cv2.imread(imagePath + file)                                                          #使用opencv讀取影象資料

        if img.shape[0]*img.shape[1] > 500000:                                                      #如果圖太大的話需要壓縮，這裡畫素的閾值可以自己設定
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

        dets = detector(img, 1)                                                                     #使用檢測運算元檢測人臉，返回的是所有的檢測到的人臉區域

        for k, d in enumerate(dets):
            rec = dlib.rectangle(d.rect.left(),d.rect.top(),d.rect.right(),d.rect.bottom())
            shape = sp(img, rec)                                                                    #獲取landmark
            face_descriptor = facerec.compute_face_descriptor(img, shape)                           #使用resNet獲取128維的人臉特徵向量
            faceArray = np.array(face_descriptor).reshape((1, 128))                                 #轉換成numpy中的資料結構
            data = np.concatenate((data, faceArray))                                                #拼接到事先準備好的data當中去
            label.append(labelName)                                                                 #儲存標籤
            cv2.rectangle(img, (rec.left(), rec.top()), (rec.right(), rec.bottom()), (0, 255, 0), 2)       #顯示人臉區域
#        cv2.waitKey(2)
#        cv2.imshow('image', img)
#        cv2.waitKey(0)

data = data[1:, :]                                                                                  #因為data的第一行是空的128維向量，所以實際儲存的時候從第二行開始
np.savetxt('faceData.txt', data, fmt='%f')                                                          #儲存人臉特徵向量合成的矩陣到本地

labelFile=open('label.txt','w')                                      
json.dump(label, labelFile)                                                                         #使用json儲存list到本地
labelFile.close()

cv2.destroyAllWindows()  
