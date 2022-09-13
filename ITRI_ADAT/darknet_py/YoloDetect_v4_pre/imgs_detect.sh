#!/bin/bash
net_size=416

main_dir='/home/jklhj/work/ADAT/ASML_CS/20220905_ASML_CS/'
imgs_dirs='20220905_ASML_CS_Val_12clips_frames_2d5'
negative_obj='screw_abnormal'

for imgs_dir in $imgs_dirs
do
  echo imgs_dir = "$imgs_dir"
  mkdir -p results/"$imgs_dir"

  for img_dir in `ls "$main_dir"'/'"$imgs_dir"'/for_test/'`
  do
     if echo $img_dir | grep -q -E 'screw_normal'
     then
       target_class='screw_normal'
     elif echo $img_dir | grep -q -E 'screw_half'
     then
       target_class='screw_abnormal'
     elif echo $img_dir | grep -q -E 'screw_loose'
     then
       target_class='screw_abnormal'
     fi

#    imgs_path="$main_dir"'/'"$imgs_dir"'/for_test/'"$img_dir"'/768x432'
    imgs_path="$main_dir"'/'"$imgs_dir"'/for_test/'"$img_dir"
    output_dir="$img_dir"

    mkdir $output_dir

    echo imgs_path $imgs_path

    python3 darknet_detect.py \
            --cfg_file config.txt \
            --resize 0.7 \
            --gpu_idx 0 \
            --thresh 0.5 \
            --negative_obj $negative_obj \
            --net_size $net_size \
            imgs_detect \
            --imgs_path "$imgs_path" \
            --output_dir "$output_dir" \
            --target_class "$target_class" \
            --save_img \
            --noshow_img 

    cp -r $output_dir results/"$imgs_dir"
    cp "$output_dir"_log.txt results/"$imgs_dir"
    rm -r $output_dir "$output_dir"_log.txt

  done
done

cd results/"$imgs_dir"
echo clip,total_frame,empty_frame,accuracy,recall,acc_avg_conf,acc_min_conf,acc_max_conf,false_rate,false_avg_conf,false_min_conf,false_max_conf > total-log.txt
for i in `ls *_log.txt`
do 
  tail -1 $i >> total-log.txt
done
cd -



