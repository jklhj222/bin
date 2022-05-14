#!/bin/bash

file=$1

file=`echo $1 | sed 's/#/!/g' | sed 's/file\//#!/g' `

megadl $file
