#!/bin/bash
# need "$lang"."$fontname"."num"."$image_format" file to be existed. (can't be too small)
# need "$lang"."$fontname"."num".box file to be existed. (be created from jTessBoxEditor)

# java -jar jTessBoxEditor.jar  :  open jTessBoxEditor
# Box Editor --> Open --> choose the training image

lang='ASML'
fontname='logo'
num='0'
image_format='jpg'
file="$lang"."$fontname".exp"$num"

echo make font_properties file:
echo -e "$fontname" 0 0 0 0 0 > font_properties

echo Run Tesseract for training:
tesseract "$file"."$image_format" "$file" nobatch box.train

echo Compute the Character Set:
unicharset_extractor "$file".box
mftraining -F font_properties -U unicharset -O "$lang".unicharset "$file".tr

echo Clustering:
cntraining "$file".tr

echo Rename Files:
mv normproto  "$lang".normproto
mv inttemp    "$lang".inttemp
mv pffmtable  "$lang".pffmtable
mv shapetable "$lang".shapetable

echo Create Tessdata:
combine_tessdata "$lang".

