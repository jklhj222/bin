#!/usr/bin/env python3


def tesseract_recog(img, exe_file):
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = exe_file
  
    code= pytesseract.image_to_string(img, lang='eng')

    return code

if __name__ == '__main__':
    from PIL import Image
    import cv2
    
    img_path = 'dis15_font3_7_7.jpg'
    exe_file = '/usr/bin/tesseract'

    img = cv2.imread(img_path)
#    img = Image.open(img_path, mode='r')

    output = tesseract_recog(img, exe_file)
    print(output, repr(output))
