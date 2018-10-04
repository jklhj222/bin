#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

# From tensorflow/models/research/

PATH_TO_CHECKPOINT='/home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/pascal_voc_seg/xception_65_train/'
PATH_TO_VIS_DIR='/home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/pascal_voc_seg/xception_65_vis/'
PATH_TO_DATASET='/home/hugh/pkg/local/tensorflow/models/research/deeplab/datasets/pascal_voc_seg/tfrecord/'

python3 deeplab/vis.py \
    --logtostderr \
    --vis_split="val" \
    --model_variant="xception_65" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --vis_crop_size=513 \
    --vis_crop_size=513 \
    --dataset="pascal_voc_seg" \
    --checkpoint_dir=${PATH_TO_CHECKPOINT} \
    --vis_logdir=${PATH_TO_VIS_DIR} \
    --also_save_raw_predictions = True \
    --dataset_dir=${PATH_TO_DATASET} 	
