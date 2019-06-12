#!/bin/bash

img_file='test.jpg'
filename=`echo $img_file | awk -F '.' '{print $1}'`
fileext=`echo $img_file | awk -F '.' '{print $2}'`

# Binarize the image
convert -monochorme "$img_file" "$filename"'_mono.'"$fileext"

# Binarize the image by threshold 
convert -threshold 50% "$img_file" "$filename"'_thres.'"$fileext"

# Turn the image into gray scale
convert -colorspace Gray "$img_file" "$filename"'_gray.'"$fileext"

# Resize the image
convert -resize 100x100 "$img_file" "$filename"'_resize.'"$fileext"
convert -resize 50%x50% "$img_file" "$filename"'_resize.'"$fileext"

# Flip the image
convert -flip "$img_file" "$filename"'_flip.'"$fileext"  # Up_Down flip
convert -flop "$img_file" "$filename"'_flop.'"$fileext"  # Left_Right flip

# Rotate the image (clockwise)
convert -rotate 30 "$img_file" "$filename"'_rotate.'"$fileext"



