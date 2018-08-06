# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="this is a test")
    
    # position argument
    parser.add_argument('position_arg1',
                        help='this is help test for position argument 1')
    parser.add_argument('position_arg2',
                        help='this is help test for position argument 2')
    parser.add_argument("square", help="display a square of a given number",
                        type=int)
    
    # optional argument
    parser.add_argument('--optional_arg1',
                        help='this is help test for optional argument 1',
                        dest='opt_arg1', 
                        default='test3')

    parser.add_argument('--set_true',
                        help='this is help test for store_true',
                        action='store_true'
                        )
    
    # if we didn't set the 'dest' parameter, 
    # the attribute name will become opt.optional_arg1
#    parser.add_argument('--optional_arg1',
#                        help='this is help test for optional argument 1',
#                        default='test3')



    args = parser.parse_args()

    print('position arg1 :', args.position_arg1)
    print('position arg2 :', args.position_arg2)
    print('square: ', args.square**2)

    print('')
    
    print('optional arg1 :', args.opt_arg1)
#    print('optional arg1 :', args.optional_arg1)

    print('set_true :', args.set_true)