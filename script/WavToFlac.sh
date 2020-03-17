#!/bin/bash

for i in `ls *wav`
do
  echo $i

  flac_file=`echo $i | awk -F '.wav' '{print $1".flac"}'`
  echo $flac_file

  sox $i $flac_file

done
