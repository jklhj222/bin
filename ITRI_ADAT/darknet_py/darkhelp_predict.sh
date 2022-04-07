#!/bin/bash

weight_dir='/mnt/sdb1/amb_project/windfarm/weights/T_windfarm_0309_Exp_HCOffice/result/'
imgs_dir='/mnt/sdb1/work/ADAT/windfarm/20220331_TN-Lab_HighView_13clips_frames/050_DeepScratch_005/768x432/'
outdir='predicts'
threshold=0.5

cfg=`ls "$weight_dir"/*.cfg`
weights=`ls "$weight_dir"/*.weights`
names=`ls "$weight_dir"/*.names`

echo $cfg $names $weights

mkdir $outdir
outdir=`pwd`'/'"$outdir"

cd $imgs_dir 
ls | xargs realpath > "$outdir"'/imgs_path.txt'
cd -

DarkHelp $cfg \
	 $weights \
	 $names \
	 -l "$outdir"'/imgs_path.txt' \
	 --json \
	 --keep \
	 --threshold $threshold \
	 --outdir $outdir  
