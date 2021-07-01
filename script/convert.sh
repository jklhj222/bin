#!/bin/bash

img_file='test.jpg'
filename=`echo $img_file | awk -F '.' '{print $1}'`
fileext=`echo $img_file | awk -F '.' '{print $2}'`

# Binarize the image
convert -monochrome "$img_file" "$filename"'_mono.'"$fileext"

# Binarize the image by threshold 
convert -threshold 50% "$img_file" "$filename"'_thres.'"$fileext"

# Turn the image into gray scale
convert -colorspace Gray "$img_file" "$filename"'_gray.'"$fileext"

# Resize the image
convert -resize 100x100\! "$img_file" "$filename"'_resize.'"$fileext"
convert -resize 50%x50% "$img_file" "$filename"'_resize.'"$fileext"

# Flip the image
convert -flip "$img_file" "$filename"'_flip.'"$fileext"  # Up_Down flip
convert -flop "$img_file" "$filename"'_flop.'"$fileext"  # Left_Right flip

# Rotate the image (clockwise)
convert -rotate 30 "$img_file" "$filename"'_rotate.'"$fileext"

# convert file into another format. (ex. jpg or png)
# the quality is from 1 (lowest image quality and highest compression) to  100 (best quality but least effective compression)
# 0 means default, The default is to use the estimated quality of your input image if it can be determined, otherwise 92.
convert -quality 90 "$img_file" "$filename"'_90.'"$fileext"

# cut image file into size x*y by x_offset*y_offset
convert "$img_file" -crop "$x"x"$y"+"$x_offset"+"$y_offset" "$filename"'_cut.'"$fileext"
