#!/usr/bin/env python3

from math import ceil

X_interval = 15
Y_interval = 15

RightUpXY  = (45, 200)
LeftDownXY = (85, 360)
intervalX  = X_interval
intervalY  = Y_interval
# A
#RightUpXY  = (21.8, 48.2)
#LeftDownXY = (89.2, 72.0)
#intervalX  = X_interval
#intervalY  = Y_interval
## B
#RightUpXY  = (198.9, 20.2)
#LeftDownXY = (262.0, 62.6)
#intervalX  = X_interval
#intervalY  = Y_interval
## C
#RightUpXY  = (-7.0, 243.7)
#LeftDownXY = (60.1, 258.1)
#intervalX  = X_interval
#intervalY  = Y_interval
# D
#RightUpXY  = (152.4, 243.7)
#LeftDownXY = (234.4, 258.1)
#intervalX  = X_interval
#intervalY  = Y_interval

width = LeftDownXY[0] - RightUpXY[0] 
height = LeftDownXY[1] - RightUpXY[1]

print('width, height: ', width, height)
print('#x, #y: ', int(width/intervalX), int(height/intervalY))

print('X: ')
Xi = 0
for X in range(ceil(width/intervalX)):
    print('{:.1f}'.format(RightUpXY[0] + X*intervalX), end=',')
    Xi += 1

print('{:.1f}'.format(LeftDownXY[0]))

print()
print('Y: ')
Yi = 0
for Y in range(ceil(height/intervalY)):
    print('{:.1f}'.format(RightUpXY[1] + Y*intervalY), end=',')
    Yi += 1

print('{:.1f}'.format(LeftDownXY[1]))

print()
print('#X:', Xi)
print('#Y:', Yi)
print('#grid:', Xi*Yi)
