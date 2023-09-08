from utils import *
from numpy import *

theta = degrees_to_radians(60.0)
alpha = degrees_to_radians(1.5)
center_depth = 70.0     
d = 200
width = haili_to_meter(4)

# 对ax+by+1=0在[xl, xh) x [yl, yh)里采样整点
def sample_dots(a, b, xl, xh, yl, yh):
    result = []
    if a >= b:
        for y in range(yl, yh):
            x = (b * y + 1) / (-a)
            if xl <= x and x < xh:
                result.append((floor(x), y))
    else:
        for x in range(xl, xh):
            y = (a * x + 1) / (-b)
            if yl <= y and y < yh:
                result.append((x, floor(y)))
    return result
    

# 寻找[points]中被ax+by+1=0探测到的点
def detected_points(points, a, b):
    result = set()
    for point in points:
        if point.detected(a, b):
            result.add((point.x, point.y))
    return result
        

thpr = diminished_angle(theta)
result = []
