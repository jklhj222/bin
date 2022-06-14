#!/usr/bin/env python3

import multiprocessing
import time

def f(x):
    return x * x

cores = multiprocessing.cpu_count() - 4
print('cores: ', cores)

pool = multiprocessing.Pool(processes=cores)

xs = range(555554663)

t0 = time.time()
list(map(f, xs))
print('t1: ', time.time() - t0)
print()

# method 1: map
t0 = time.time()
pool.map(f, xs) # prints [0, 1, 4, 9, 16]
print('t2: ', time.time() - t0)
print()

# method 2: imap
t0 = time.time()
for y in pool.imap(f, xs):
    pass
#    print(y)      # 0, 1, 4, 9, 16, respectively
print('t3 ', time.time() - t0)
print()


# method 3: imap_unordered
t0 = time.time()
for y in pool.imap_unordered(f, xs):
   pass 
#   print(y)      # may be in any order
print('t4 ', time.time() - t0)
