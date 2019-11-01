#!/bin/bash

python3 train.py --save-epoch 2000 --eval-epoch 3000 --lr 0.001 --lr-steps 3000 6000 9000 --epochs 10000 
