#!/bin/bash

train_val_ratio=0.9

line=`wc train_orig.txt | awk '{print $1}'`
echo 'total_data = '$line

train_num=`echo | awk '{print int(line*train_val_ratio)}' line=$line train_val_ratio=$train_val_ratio `
echo 'train_data = '$train_num

val_num=`echo $line - $train_num | bc`
echo 'val_data = '$val_num


shuf train_orig.txt | shuf | shuf > total.txt

head -"$train_num" total.txt > train.txt
tail -"$val_num" total.txt > val.txt
