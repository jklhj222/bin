#!/bin/bash

for i in `ls ./ | grep -v $0`
do
  tar zxvf "$i"
done
