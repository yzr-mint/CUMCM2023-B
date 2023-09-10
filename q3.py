from utils import *
from numpy import *
from draw_result import *

def get_lines(guide, depths, theta):
    # result格式为[(a,b)] (线的参数)
    result = []

    xl, yl = 0, 0
    points_dic, xr, yr = depth_to_point_dic(depths, theta)
    sample_points = get_sample_diag(guide[0], guide[1], xl, xr, yl, yr)    
    undetected_point_index = 0
    choose_point_index = 0

    while(1):
        # 找下一个测线经过的点
        undetected_point = points_dic[sample_points[undetected_point_index]]
        while(points_dic[sample_points[choose_point_index]].close_enough(undetected_point.x, undetected_point.y) == False):
            choose_point_index += 1
        while(points_dic[sample_points[choose_point_index]].close_enough(undetected_point.x, undetected_point.y)):
            choose_point_index += 1
            if(choose_point_index == len(sample_points)):
                choose_point_index -= 1
                a, b = get_nor(guide[1], -guide[0], sample_points[choose_point_index][0], sample_points[choose_point_index][1])
                result.append((a, b))
                return result

        choose_point_index -= 1
        a, b = get_nor(guide[1], -guide[0], sample_points[choose_point_index][0], sample_points[choose_point_index][1])
        result.append((a, b))

        # 找下一个无法被探测的点
        while(undetected_point.detected_by(a, b) == False):
            undetected_point_index += 1
            undetected_point = points_dic[sample_points[undetected_point_index]]
        while(undetected_point.detected_by(a, b)):
            undetected_point_index += 1
            if undetected_point_index == len(sample_points):
                return result
            undetected_point = points_dic[sample_points[undetected_point_index]]


if __name__ == '__main__':
    theta = degrees_to_radians(60.0)
    alpha = degrees_to_radians(1.5)
    inte_time = 5
    center_depth = 110
    d = 200
    thpr = diminished_angle(theta)

    guide = get_nor(0, -200, 50, 100)   
    a = get_depths(4, 2, center_depth, alpha)
    b = depth_to_numpy(a)
    depths = interpolate(b, inte_time)

    result = get_lines(guide, depths, thpr)
    print(len(result))
    print(result)

    result = array(result)
    result = result * (2 ** inte_time)
    line_in_grads(100, 200, result)
    
