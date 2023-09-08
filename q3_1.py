from utils import *
from numpy import *

def get_lines():
    theta = degrees_to_radians(60.0)
    alpha = degrees_to_radians(1.5)
    center_depth = 110   
    d = 200
    thpr = diminished_angle(theta)

    guide = (0, -1)
    # [(a,b)] (一堆线)
    result = []

    xl = 0
    yl = 0
    a=get_depths(4, 2, center_depth, alpha)
    points_dic, xr, yr = depth_to_point_dic(a, thpr)

    sample_points = get_sample_points(guide[0], guide[1], xl, xr, yl, yr)

    undetected_point_index = 0
    choose_point_index = 0
    sign = 1

    while(sign):
        # 找下一个测线经过的点
        undetected_points = sample_points[undetected_point_index]
        while(points_dic[sample_points[choose_point_index]].close_enough(undetected_points[0], undetected_points[1])):
            choose_point_index += 1
            if(choose_point_index == len(sample_points)):
                choose_point_index -= 1
                a, b = get_orth(guide[1], -guide[0], sample_points[choose_point_index][0], sample_points[choose_point_index][1])
                result.append((a, b))
                return result

        choose_point_index -= 1
        a, b = get_orth(guide[1], -guide[0], sample_points[choose_point_index][0], sample_points[choose_point_index][1])
        result.append((a, b))

        # 找下一个无法被探测的点
        undetected_point = points_dic[sample_points[undetected_point_index]]
        while(undetected_point.detected_by(a, b)):
            undetected_point_index += 1
            if undetected_point_index == len(sample_points):
                return result
            undetected_point = points_dic[sample_points[undetected_point_index]]
        choose_point_index += 1

result = get_lines()
print(result)


