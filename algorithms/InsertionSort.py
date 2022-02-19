import time

from colors import *

def insertion_sort(data, renderData, timeTick):
    for i in range(len(data)-1):
        if data[i] < data[i-1]:
            n = i
            while data[n] < data[n-1]:
                data[n], data[n-1] = data[n-1], data[n]
                renderData(data, [BLUE for x in range(len(data))])
                time.sleep(timeTick)
                if n > -1: n-=1
    renderData(data, [BLUE for x in range(len(data))])
    
