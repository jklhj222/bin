#!/usr/bin/env python3
import dlib
import cv2
import imutils
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--img_file', default=None)
parser.add_argument('--show_img', 
                    default=False, 
                    help='default: False',
                    action='store_true')

args = parser.parse_args()

img_file = args.img_file

img = cv2.imread(img_file)
img = imutils.resize(img, width=1280)
detector = dlib.get_frontal_face_detector()

face_rects, scores, idx = detector.run(img, 0, -1)

for i, d in enumerate(face_rects):
    x1 = d.left()
    y1 = d.top()
    x2 = d.right()
    y2 = d.bottom()
    text = "%2.2f(%d)" % (scores[i], idx[i])

    img_cut = img[y1:y2, x1:x2]
	
    cv2.imwrite('./cut/' + str(i) + '.jpg', img_cut)

    if args.show_img:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)

        cv2.putText(img, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX,
          0.7, (255, 255, 255), 1, cv2.LINE_AA)


        cv2.imshow("Face Detection", img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
