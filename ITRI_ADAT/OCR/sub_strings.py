#!/usr/bin/env python3
""" Created on Tue Apr 30 09:17:06 2019 @author: jklhj """


def sub_strings(test_string, sub_min):
    
    strings = []
    for i in range(len(test_string)):
        if i>0: test_string = test_string[1:]
        
        str_tmp = ''
        for char in test_string:
            
            print(str_tmp)
            
            str_tmp += char
            
            if len(str_tmp) >= sub_min: strings.append(str_tmp)
            
        print()
        print(strings)
        
    return list(set(strings))
    
if __name__ == '__main__':
    test_string = 'ABCDEFGH01234567890ABCDE' 
    sub_min = 5
    strings = sub_strings(test_string, sub_min)
    