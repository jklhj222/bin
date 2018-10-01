#!/bin/bash

for i in `ls ./`
do
  tar zcvf "$i".tar.gz "$i"
done
