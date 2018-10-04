#!/bin/bash
# From tensorflow/models/research/

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

python3 deeplab/train.py \
    --logtostderr \
    --training_number_of_steps=150000 \
    --train_split="train" \
    --model_variant="xception_65" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --train_crop_size=513 \
    --train_crop_size=513 \
    --train_batch_size=4 \
    --min_resize_value=513 \
    --max_resize_value=513 \
    --resize_factor=16 \
    --dataset="ade20k" \
    --num_clones=2 \
    --ps_tasks=1 \
    --tf_initial_checkpoint=/home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/Pretrained_models/xception_65/model.ckpt \
    --train_logdir=/home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/ADE20K/xception_65_train/ \
    --dataset_dir=/home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/ADE20K/tfrecord/ 2>&1 | tee /home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/ADE20K/xception_65_train/train_20181002.log 
