#!/bin/bash

model_dir='/mnt/sdb1/amb_project/ASML_CS_new2/weights/'

for w in `ls $model_dir`
do
  echo "$w"
  sed -i 's/model_dir/'"$w"'/g' config.txt

  ./imgs_detect.sh
  
  sed -i 's/'"$w"'/model_dir/g' config.txt
  mv results results_"$w"
done
