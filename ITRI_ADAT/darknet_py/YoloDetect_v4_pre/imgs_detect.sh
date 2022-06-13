#!/bin/bash
#target_class='MV-0_Lock'
#target_class='MV-0_Unlock'
net_size=1024

main_dir='/home/jklhj/work/ADAT/CPC/OringPin/'
imgs_dirs='20220606_CPC_OringPin_32clips_frames'
negative_obj='oring_noexist pin_noexist'

for target_class in oring_exist oring_noexist pin_exist pin_noexist 
do

# customerize
cd $main_dir'/'$imgs_dirs
if [ "$target_class" = 'oring_exist' ]
then
    ./change_for_test.sh for_test_oringexist
elif [ "$target_class" = 'oring_noexist' ]
then
    ./change_for_test.sh for_test_oringnoexist
elif [ "$target_class" = 'pin_exist' ]
then
    ./change_for_test.sh for_test_pinexist
elif [ "$target_class" = 'pin_noexist' ]
then
    ./change_for_test.sh for_test_pinnoexist
fi
cd -
#

#if [ "$net_size" = '416' ]
#then
#    imgs_dirs='labelclip_rotate_-5deg labelclip_rotate_5deg labelclip_rotate_-10deg labelclip_rotate_10deg labelclip_rotate_-15deg labelclip_rotate_15deg labelclip_rotate_-20deg labelclip_rotate_20deg  labelclip_rotate_-25deg labelclip_rotate_25deg labelclip_rotate_-30deg labelclip_rotate_30deg'
#elif [ "$net_size" = '1024' ]
#then
#    imgs_dirs='labelclip_rotate_0deg'
#fi

#for imgs_dir in labelclip_rotate_-5deg labelclip_rotate_5deg labelclip_rotate_-10deg labelclip_rotate_10deg labelclip_rotate_-15deg labelclip_rotate_15deg labelclip_rotate_-20deg labelclip_rotate_20deg  labelclip_rotate_-25deg labelclip_rotate_25deg labelclip_rotate_-30deg labelclip_rotate_30deg 
#for imgs_dir in labelclip_rotate_0deg
for imgs_dir in $imgs_dirs
do
  echo imgs_dir = "$imgs_dir"
  mkdir -p results/"$imgs_dir"

  for img_dir in `ls "$main_dir"'/'"$imgs_dir"'/for_test/'`
  do

#    imgs_path="$main_dir"'/'"$imgs_dir"'/for_test/'"$img_dir"'/768x432'
    imgs_path="$main_dir"'/'"$imgs_dir"'/for_test/'"$img_dir"
    output_dir="$img_dir"

    mkdir $output_dir

    echo $imgs_path

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
            --save_img \
            --target_class "$target_class" \
            --noshow_img 

    cp -r $output_dir results/"$imgs_dir"
    cp "$output_dir"_log.txt results/"$imgs_dir"
    rm -r $output_dir "$output_dir"_log.txt

  done
done

done
