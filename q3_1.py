from utils import *
from numpy import *

theta = degrees_to_radians(60.0)
alpha = degrees_to_radians(1.5)
center_depth = 70.0     
d = 200
thpr = diminished_angle(theta)

guide = (0, 1)
# [(a,b)] (一堆线)
result = []

xl = 0
yl = 0
points, xr, yr = get_points(4, 2, get_depths(4, 2, 110, alpha), thpr, unit = 37.04)

sample_points = get_sample_points(guide[0], guide[1], xl, xr, yl, yr)

undetected_point_index = 0
choose_point_index = 0
S = []
while(1):
    # 找下一个测线经过的点
    undetected_points = sample_points[undetected_point_index]
    while(sample_points[choose_point_index].close_enough(undetected_points.x, undetected_points.y)):
        choose_point_index += 1
    choose_point_index -= 1
    S.append(choose_point_index)

    # 找下一个无法被探测的点
    


