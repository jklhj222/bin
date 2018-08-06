# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count


## 單執行緒
def single_core():
    import time
    from concurrent.futures import ProcessPoolExecutor
    from multiprocessing import cpu_count

    def gcd(pair):
        a,b = pair
        low = min(a,b)
        for i in range(low,0,-1):
            if a % i == 0 and b % i == 0:
                return i
    
    numbers = [(89937224,53452411),(97432894,43939284),(95938272,94910833),
               (7398473,47382942),(85938272,90493759)]
    start = time.time()
    print('cpu count :', cpu_count())
    results = list(map(gcd,numbers))
    end = time.time()
    print(results)
    print('Took %.3f secondes'%(end-start), 'for single core')

single_core()
print('')

def gcd(pair):
    a,b = pair
    low = min(a,b)
    for i in range(low,0,-1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(89937224,53452411),(97432894,43939284),(95938272,94910833),
           (7398473,47382942),(85938272,90493759)]
start = time.time()
print('cpu count :', cpu_count())
pool = ProcessPoolExecutor(max_workers=cpu_count())
results = list(pool.map(gcd,numbers))
end = time.time()
print(results)
print('Took %.3f secondes'%(end-start), 'for multiple cores')

