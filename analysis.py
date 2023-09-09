from utils import *

def length_sum(lines, xsize, ysize):
    sum = 0
    for line in lines:
        cross_point = cross(ysize, xsize, line[0], line[1])
        sum += sqrt((cross_point[0][0] - cross_point[1][0]) ** 2 + (cross_point[0][1] - cross_point[1][1]) ** 2)
    return sum    

def 