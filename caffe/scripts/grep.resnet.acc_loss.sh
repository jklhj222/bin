#!/bin/bash

test_interval=`grep test_inter log | awk '{print $2}'`

grep Test log | grep "#0" | grep accu | awk '{print test_int*(NR-1)+50"   "$11}' test_int=$test_interval > top1.acc.dat
grep Test log | grep "#1" | grep accu | awk '{print test_int*(NR-1)+50"   "$11}' test_int=$test_interval > top5.acc.dat

grep loss log | grep Iteration | awk '{print $6"   "$NF}' > loss.dat

xmgrace -autoscale xy -free -pexec "arrange (2, 1, .1, .1, .1)" -graph 0 top1.acc.dat -graph 0 top5.acc.dat -graph 1 loss.dat
