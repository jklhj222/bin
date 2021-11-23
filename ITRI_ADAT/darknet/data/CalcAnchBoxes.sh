#!/bin/bash

python3 CalcAnchBoxes.py --yolo_size 416 \
                         --n_clusters 6 \
                         --img_type jpg \
                         from_train_file \
                         --train_file train.txt
