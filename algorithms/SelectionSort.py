import time

from colors import *

def selection_sort(data, renderData, tickTime):
    for i in range(len(data)):
        minimum = i
        for j in range(i+1, len(data)):
            if data[j] < data[minimum]:
                minimum = j
        renderData(data, [LIGHT_GREEN if x == minimum else RED if x == i else BLUE for x in range(len(data))])
        data[i], data[minimum] = data[minimum], data[i]
        time.sleep(tickTime)
    renderData(data, [BLUE for x in range(len(data))])
    
