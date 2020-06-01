#transpose 參數
#0 = 90 CounterCLockwise and Vertical Flip (default)
#1 = 90 Clockwise 90 degree
#2 = 90 CounterClockwise 90 degree
#3 = 90 Clockwise and Vertical Flip


ffmpeg -i INPUT.mov -vf "transpose=1" OUTPUT.mov
