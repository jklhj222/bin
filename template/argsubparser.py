#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(prog='PROG')

parser.add_argument('--foo', action='store_true', help='foo help')

subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('--bar', type=int, help='bar help')



args = parser.parse_args()

print(args.foo)
print(args.bar)
