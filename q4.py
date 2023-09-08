from utils import *
from q3_1 import *

def iteration(points, lines, xsize, ysize, theta, theta_prime):
    etas = get_eta(points, lines, xsize, ysize)
    new_lines = []
    gamma = 0.05
    for i in range(1, len(etas)):
        a, b = lines[i][0], lines[i][1]
        new_a, new_b = a, b
        k = get_k(a, b)
        if abs(k) < 1:
            upper_sum, lower_sum = 0, 0
            if k > 0:
                lower_sum = weight_sum(etas[:len(etas) // 2])
                upper_sum = weight_sum(etas[len(etas) // 2:])
            else:
                etas_reverse = etas[::-1]
                lower_sum = weight_sum(etas_reverse[:len(etas) // 2])
                upper_sum = weight_sum(etas_reverse[len(etas) // 2:])
            x1, y1 = get_point_with_x(a, b, 0)
            x2, y2 = get_point_with_x(a, b, xsize)
            y1 += gamma * lower_sum
            y2 += gamma * upper_sum
            new_a, new_b = normalize(x1, y1, x2, y2)
        else: 
            upper_sum, lower_sum = 0, 0
            if k > 0:
                lower_sum = weight_sum(etas[:len(etas) // 2])
                upper_sum = weight_sum(etas[len(etas) // 2:])
            else:
                etas_reverse = etas[::-1]
                lower_sum = weight_sum(etas_reverse[:len(etas) // 2])
                upper_sum = weight_sum(etas_reverse[len(etas) // 2:])
            x1, y1 = get_point_with_y(a, b, 0)
            x2, y2 = get_point_with_y(a, b, ysize)
            x1 += gamma * lower_sum
            x2 += gamma * upper_sum
            new_a, new_b = normalize(x1, y1, x2, y2)
            
        if len(get_sample_points(new_a, new_b, 0, xsize, ysize)):
            new_lines.append((new_a, new_b))
    return new_lines


theta = degrees_to_radians(60.0)
theta_prime = diminished_angle(theta)
guide = (7, -1)
xsize = 200
ysize = 250

depths = read_excel_to_points(filename = '附件.xlsx')
points = depth_to_point_set(depths, theta)
depths = depth_to_numpy(depths)
# depths = interpolate(depths, 4)

lines = get_lines(guide, depths, theta_prime)

epoch = 20

for i in range(epoch):
    lines = iteration(points, lines, xsize, ysize, theta, theta_prime)