#!/bin/bash
#target_class='MV-0_Lock'
target_class='MV-0_Unlock'
net_size=416

main_dir='/home/jklhj/work/ADAT/Innolux/innolux_rotate_img_20220607'

## customerize
cd $main_dir
if [ "$target_class" = 'MV-0_Lock' ]
then
    ./change_for_test.sh for_test_Lock
elif [ "$target_class" = 'MV-0_Unlock' ]
then
    ./change_for_test.sh for_test_Unlock
fi
cd -
##

if [ "$net_size" = '416' ]
then
    imgs_dirs='labelclip_rotate_-5deg labelclip_rotate_5deg labelclip_rotate_-10deg labelclip_rotate_10deg labelclip_rotate_-15deg labelclip_rotate_15deg labelclip_rotate_-20deg labelclip_rotate_20deg  labelclip_rotate_-25deg labelclip_rotate_25deg labelclip_rotate_-30deg labelclip_rotate_30deg'
elif [ "$net_size" = '1024' ]
then
    imgs_dirs='labelclip_rotate_0deg'
fi

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
            --net_size "$net_size" \
            imgs_detect \
            --imgs_path "$imgs_path" \
            --output_dir "$output_dir" \
            --save_img \
            --target_class "$target_class" \
            --noshow_img 

  done
  cp -r *MV0* results/"$imgs_dir"/
  rm -r *MV0* 
#  mv *MV0* results/"$imgs_dir"/
done

