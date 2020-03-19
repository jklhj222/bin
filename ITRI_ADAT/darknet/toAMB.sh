#!/bin/bash

amb_main_path='/mnt/sda1/amb_project'
main_project='Siemens'
sub_project='yolo_training'

source_videos='/mnt/sda1/work/Siemens_motor_20200221/Nokia8.1_20200311/videos'

main_project_dir="$amb_main_path"/"$main_project"
sub_project_dir="$amb_main_path"/"$main_project"/"$sub_project"

if [ ! -e "$main_project_dir" ]
then
    mkdir -p "$main_project_dir"
fi

cd "$main_project_dir"

mkdir dataset  labelclip  log  sourceclip  tasks  trained_weights  weights

cd -

# dataset
cd "$main_project_dir"'/dataset'
mkdir "$sub_project"
cd -
cp data/adat.names "$main_project_dir"'/dataset/'"$sub_project"'/label.names'
cp data/train.txt "$main_project_dir"'/dataset/'"$sub_project"'/train.txt'
cp data/val.txt "$main_project_dir"'/dataset/'"$sub_project"'/val.txt'

# sourceclip
#cp -r "$source_videos"'/*' sourceclip/

# log
cp log "$main_project_dir"'/log/'"$sub_project"'.log'

# tasks
cd "$main_project_dir"'/tasks'
mkdir "$sub_project"
cd -
pwd
cp cfg/adat.data "$main_project_dir"'/tasks/'"$sub_project"'/task.data'
cp cfg/yolov3.cfg "$main_project_dir"'/tasks/'"$sub_project"'/train.cfg'
cp cfg/yolov3_test.cfg "$main_project_dir"'/tasks/'"$sub_project"'/test.cfg'
echo test0
pwd

# trained_weights
cd "$main_project_dir"'/trained_weights'
mkdir "$sub_project"
cd -
echo test
pwd
cd backup
pwd
for weight in `ls`
do
  newname=`echo "$weight" | awk -F '_' '{print "train_"$2}'`
  echo $weight $newname

  cp "$weight" "$main_project_dir"'/trained_weights/'"$sub_project"'/'"$newname"
done
cd ..
pwd

# weights
cd "$main_project_dir"'/weights'
mkdir "$sub_project"
cd -
cp data/adat.names "$main_project_dir"'/weights/'"$sub_project"'/label.names'
cp cfg/adat.data "$main_project_dir"'/weights/'"$sub_project"'/task.data'
cp cfg/yolov3_test.cfg "$main_project_dir"'/weights/'"$sub_project"'/test.cfg'
cp backup/*best* "$main_project_dir"'/weights/'"$sub_project"'/train_best.weights'





