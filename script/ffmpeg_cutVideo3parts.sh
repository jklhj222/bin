#!/bin/bash

for i in `ls *.mp4`
do
  input_file="$i"
  echo $input_file
  output_prefix=`echo $input_file | awk -F '.mp4' '{print $1}'`'_part'
  echo $output_prefix
#  output_prefix="output_part"

  # 获取视频时长（以秒为单位）
  duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$input_file")
  echo $duration

  # 计算每部分的时长
  part_duration=$(echo "$duration / 3" | bc)

  # 分割视频
  for i in {1..3}
  do
    start_time=$(echo "$part_duration * ($i - 1)" | bc)
    output_file="${output_prefix}${i}.mp4"
    ffmpeg -i "$input_file" -ss "$start_time" -t "$part_duration" -c copy "$output_file"
  done

  echo "分割完成，生成文件：${output_prefix}1.mp4，${output_prefix}2.mp4，${output_prefix}3.mp4"

done

