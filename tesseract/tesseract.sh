#!/bin/bash
#tesseract imagename outputbase [-l lang] [-psm pagesegmode] [configfile…]

image='test.jpg'
output='output.txt'
lang='eng'

tesseract "$image" "$output" -l "$lang"
