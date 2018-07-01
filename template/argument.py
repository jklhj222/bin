#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 15:24:44 2018 @author: jklhj
"""

import argparse
parser = argparse.ArgumentParser()
#parser.parse_args()

#parser.add_argument("echo", help="echo the string you use here")
parser.add_argument("square", help="display a square of a given number", 
                    type=int)

args = parser.parse_args()

#print(args.echo)
print(args.square**2)