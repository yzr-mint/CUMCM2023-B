from utils import *
from q3_1 import *
from draw_result import *

Tolerent = 5

def iteration(points, lines, xsize, ysize, dir, gamma):
    """
    dir = 1, 往右
    dir = -1, 往左
    """
    etas = get_eta(points, lines, xsize, ysize)
    new_lines = [lines[0]]
    for i in range(1, len(etas)):
        a, b = lines[i][0], lines[i][1]
        new_a, new_b = a, b
        k = get_k(a, b)
        point_size = len(etas[i])
        if abs(k) < 1:
            upper_sum, lower_sum = 0, 0
            if k > 0:
                lower_sum = dir * weight_sum(etas[i][:point_size // 2])
                upper_sum = dir * weight_sum(etas[i][point_size // 2:])
            else:
                eta_reverse = etas[i][::-1]
                lower_sum = dir * weight_sum(eta_reverse[:point_size // 2])
                upper_sum = dir * weight_sum(eta_reverse[point_size // 2:])
            x1, y1 = get_point_with_x(a, b, 0)
            x2, y2 = get_point_with_x(a, b, xsize)
            y1 += gamma * lower_sum
            y2 += gamma * upper_sum
            new_a, new_b = normalize(x1, y1, x2, y2)
        else: 
            upper_sum, lower_sum = 0, 0
            if k > 0:
                lower_sum = dir * weight_sum(etas[i][:point_size // 2])
                upper_sum = dir * weight_sum(etas[i][point_size // 2:])
            else:
                eta_reverse = etas[i][::-1]
                lower_sum = dir * weight_sum(eta_reverse[:point_size // 2])
                upper_sum = dir * weight_sum(eta_reverse[point_size // 2:])
            x1, y1 = get_point_with_y(a, b, 0)
            x2, y2 = get_point_with_y(a, b, ysize)
            x1 += gamma * lower_sum
            x2 += gamma * upper_sum
            new_a, new_b = normalize(x1, y1, x2, y2)
        
        if len(get_sample_points(new_a, new_b, 0, xsize, 0, ysize)):
            new_lines.append((new_a, new_b))
    return new_lines


theta = degrees_to_radians(60.0)
theta_prime = diminished_angle(theta)
# 经过中心点的直线. 7和-1可以改
guide = get_nor(-1, 1, 100, 125)
xsize = 200
ysize = 250

depths = read_excel_to_points(filename = '附件.xlsx')
points = depth_to_point_set(depths, theta)
depths = depth_to_numpy(depths)
# depths = interpolate(depths, 4)

lines = get_lines(guide, depths, theta_prime)

pre_result = 10000
lines_num = len(lines)
sign = 1
tolerent = Tolerent
epoch = 0
all_results = []
gamma = 0.00001
print("gamma = ", gamma)

epoch = 5
for i in range(epoch):
    print("epoch %d" % i)
    lines = iteration(points, lines, xsize, ysize, 1, gamma)
    print("number of lines: %d" % len(lines))
    all_results.append(lines)

    lines = iteration(points, lines[::-1], xsize, ysize, -1, gamma)
    print("number of lines: %d" % len(lines))
    all_results.append(lines)


'''
while(tolerent):
    epoch += 1
    print("epoch %d" % epoch)
    lines = iteration(points, lines, xsize, ysize, 1)
    print("number of lines: %d" % len(lines))
    all_results.append(lines)

    lines = iteration(points, lines[::-1], xsize, ysize, -1)
    print("number of lines: %d" % len(lines))
    all_results.append(lines)
    
    lines_num = len(lines)
    if pre_result == lines_num:
        tolerent -= 1
    else:
        tolerent = Tolerent
        pre_result = lines_num
'''
many_line_in_grads(200, 250, all_results)