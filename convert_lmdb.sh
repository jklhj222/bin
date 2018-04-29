#!/bin/bash

rm -r train_lmdb
convert_imageset --resize_height=300 --resize_width=300 --shuffle Total_png/ train_label.dat train_lmdb
