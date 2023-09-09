from utils import *

def length_sum(lines, xsize, ysize):
    sum = 0
    for line in lines:
        sum += in_length(ysize, xsize, line[0], line[1])
    return sum    

def 