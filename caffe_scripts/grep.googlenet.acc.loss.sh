#!/bin/bash

read -p 'log file name ? ' filename

start_iter=`grep Iter log | head -1 | awk '{print $6}'`

test_interval=`grep test_interval "$filename" | tail -1 | awk '{print $2}'`
display=`grep display "$filename" | tail -1 | awk '{print $2}'`

echo $start_iter
echo $test_interval
echo $display

grep top-1 "$filename" | grep Test | grep loss1 | nl | awk '{print $1*test_interval"   "$12}' test_interval=$test_interval > acc_top1_test.dat
grep top-5 "$filename" | grep Test | grep loss1 | nl | awk '{print $1*test_interval"   "$12}' test_interval=$test_interval > acc_top5_test.dat
echo " " >> acc_top1_test.dat
echo " " >> acc_top5_test.dat
grep top-1 "$filename" | grep Test | grep loss2 | nl | awk '{print $1*test_interval"   "$12}' test_interval=$test_interval >> acc_top1_test.dat
grep top-5 "$filename" | grep Test | grep loss2 | nl | awk '{print $1*test_interval"   "$12}' test_interval=$test_interval >> acc_top5_test.dat
echo " " >> acc_top1_test.dat
echo " " >> acc_top5_test.dat
grep top-1 "$filename" | grep Test | grep loss3 | nl | awk '{print $1*test_interval"   "$12}' test_interval=$test_interval >> acc_top1_test.dat
grep top-5 "$filename" | grep Test | grep loss3 | nl | awk '{print $1*test_interval"   "$12}' test_interval=$test_interval >> acc_top5_test.dat

grep loss1 "$filename" | grep Train | nl | awk '{print ($1-1)*display+start_iter"   "$12}' display=$display start_iter=$start_iter > loss_train.dat
echo " " >> loss_train.dat
grep loss2 "$filename" | grep Train | nl | awk '{print ($1-1)*display+start_iter"   "$12}' display=$display start_iter=$start_iter >> loss_train.dat
echo " " >> loss_train.dat
grep loss3 "$filename" | grep Train | nl | awk '{print ($1-1)*display+start_iter"   "$12}' display=$display start_iter=$start_iter >> loss_train.dat

grep loss1 "$filename" | grep Test | grep -v top | nl | awk '{print ($1-1)*test_interval"   "$12}' test_interval=$test_interval > loss_test.dat
echo " " >> loss_test.dat
grep loss2 "$filename" | grep Test | grep -v top | nl | awk '{print ($1-1)*test_interval"   "$12}' test_interval=$test_interval >> loss_test.dat
echo " " >> loss_test.dat
grep loss3 "$filename" | grep Test | grep -v top | nl | awk '{print ($1-1)*test_interval"   "$12}' test_interval=$test_interval >> loss_test.dat

xmgrace -para ~/bin/caffe_scripts/acc_loss_googlenet.par -autoscale xy -free -pexec "arrange (4, 1, .1, .1, .1)" -graph 0 acc_top1_test.dat -graph 1 acc_top5_test.dat -graph 2 loss_train.dat -graph 3 loss_test.dat
