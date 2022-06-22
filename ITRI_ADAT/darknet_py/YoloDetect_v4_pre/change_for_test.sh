#!/bin/bash

#test_dir='for_test_Lock'
#test_dir='for_test_Unlock'
test_dir=$1

if [ -d "for_test" ]
then
  rm -r for_test
fi

cp -r "$test_dir" ./for_test

cd ..
