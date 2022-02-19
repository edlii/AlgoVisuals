import time

from colors import *

def quick_sort(data, start, end, renderData, tickTime):
    if start < end:
        p = partition(data, start, end, renderData, tickTime)
        quick_sort(data, start, p - 1, renderData, tickTime)
        quick_sort(data, p + 1, end, renderData, tickTime)

def partition(data, start, end, renderData, tickTime):
    pivot_index = start
    pivot = data[pivot_index]
    while start < end:
        while start < len(data) and data[start] <= pivot:
            start += 1
        while data[end] > pivot:
            end -= 1
        if start < end:
            renderData(data, [YELLOW if x == start else RED if x == end else BLUE for x in range(len(data))])
            data[start], data[end] = data[end], data[start]
    renderData(data, [YELLOW if x == pivot_index else RED if x == end else BLUE for x in range(len(data))])       
    data[end], data[pivot_index] = data[pivot_index], data[end]
    renderData(data, [BLUE for x in range(len(data))])
    return end