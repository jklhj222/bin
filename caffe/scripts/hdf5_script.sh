#!/bin/bash
# manipulate header path, before building caffe on debian jessie
# usage:
#1. cd root of caffe
#2. bash <this_script>
#3. build

# transformations :
#  #include "hdf5/serial/hdf5.h" -> #include "hdf5/serial/hdf5.h"
#  #include "hdf5/serial/hdf5_hl.h" -> #include "hdf5/serial/hdf5_hl.h"

find . -type f -exec sed -i -e 's^"hdf5/serial/hdf5.h"^"hdf5/serial/hdf5.h"^g' -e 's^"hdf5/serial/hdf5_hl.h"^"hdf5/serial/hdf5_hl.h"^g' '{}' \;
