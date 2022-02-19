import time

from colors import *

def insertion_sort(data, renderData, timeTick):
    for j in range(1, len(data)):
        key = data[j]
        i = j - 1
        while i >= 0 and data[i] > key:
            data[i+1] = data[i]
            renderData(data, [PURPLE if x == i else RED if x == i-1 else BLUE for x in range(len(data))])
            i = i - 1
        data[i+1] = key
    renderData(data, [BLUE for x in range(len(data))])


    
