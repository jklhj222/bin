#!/bin/bash

read -p 'log file name? ' filename

start_iter=`grep Iter "$filename" | head -2 | tail -1 | awk '{print $6}'`
echo $start_iter

test_interval=`grep test_interval "$filename" | tail -1 | awk '{print $2}'`
display=`grep display "$filename" | tail -1 | awk '{print $2}'`

echo $start_iter
echo $test_interval
echo $display

grep accu "$filename"  | grep Test  | nl | awk '{print (($1-1)*test_interval+start_iter)+10"   "$12}'  start_iter=$start_iter test_interval=$test_interval  > accuracy.dat # plus 10 in interation if for mathing the graph with loss
grep loss "$filename"  | grep Train | nl | awk '{print $1*display+start_iter"   "$16}' start_iter=$start_iter display=$display > loss_train.dat
grep loss "$filename"  | grep Test  | nl | awk '{print ($1-1)*test_interval+start_iter"   "$16}' start_iter=$start_iter test_interval=$test_interval > loss_test.dat

xmgrace -para ~/bin/caffe_scripts/acc_loss.par -autoscale xy -free -pexec "arrange (2, 1, .1, .1, .1)" \
     -graph 0 accuracy.dat -graph 1 loss_train.dat -graph 1 loss_test.dat
