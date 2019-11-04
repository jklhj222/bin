#!/bin/bash

filename=trainval.json.bk

num_img=6
num_category=2

sed -i 's/\"image_id\":\ 0/\"image_id\": '"$num_img"'/g' "$filename"
sed -i 's/\"category_id\":\ 0/\"category_id\": '"$num_category"'/g' "$filename"

img_line=`cat -n "$filename" | grep -A 4 images | tail -1 | awk '{print $1}'`
sed -i ''"$img_line"'s/0/'"$num_img"'/g' $filename

cat_line=`cat -n "$filename" | grep -A 3 categories | tail -1 | awk '{print $1}'`
sed -i ''"$cat_line"'s/0/'"$num_category"'/g' $filename
