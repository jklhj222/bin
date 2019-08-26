#!/usr/bin/env python3
""" Created on Thu Aug 22 17:32:39 2019 @author: jklhj """

import logging
from functools import wraps

    
def use_logging(func):
    @wraps(func)
    def wrapper():
        logging.warning("%s is running" % func.__name__)
        
        return func()
    
    return wrapper

@use_logging
def foo():
    print('i am foo')
    

foo()
print()
# cancel the decorator
foo.__wrapped__()


