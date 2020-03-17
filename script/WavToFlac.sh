#!/bin/bash

space2underline()
{
startDir=.

for arg in "$@" 
do
  find $startDir \( -name "* *" -o -name "* *" \) -print |
  while read old
  do
    new=$(echo "$old" | tr -s '\011' ' ' | tr -s ' ' '_')
    mv "$old" "$new"
  done
done
}
space2underline d f # Renames your directories with spaces first, then files

for i in `ls *wav`
do


  echo $i

  flac_file=`echo $i | awk -F '.wav' '{print $1".flac"}'`
  echo $flac_file

  sox $i $flac_file

done
