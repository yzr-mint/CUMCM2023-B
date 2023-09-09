from utils import *
from q3_1 import *
from draw_result import *
import pickle

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

# depth 是一个numpy矩阵, guide_ab是guide的方向, epoch是训练次数
def train(depths, guide_ab, epoch, theta):
    xsize = depths.shape[0]
    ysize = depths.shape[1]
    guide = get_nor(guide_ab[0], guide_ab[1], xsize/2, ysize/2)
    points = depth_to_point_set(depths, theta)

    theta_prime = diminished_angle(theta)
    lines = get_lines(guide, depths, theta_prime)
    all_results = []
    gamma = 0.005
    print("gamma = ", gamma)
    print(len(lines))

    for i in range(epoch):
        print("epoch %d" % i)
        lines = iteration(points, lines, xsize, ysize, 1, gamma)
        print("number of lines: %d" % len(lines))
        all_results.append(lines)

        lines = iteration(points, lines[::-1], xsize, ysize, -1, gamma)
        print("number of lines: %d" % len(lines))
        all_results.append(lines)

    many_line_in_grads(xsize, ysize, all_results)
    # 将列表保存为二进制文件
    with open('my_list.pkl', 'wb') as file:
        pickle.dump(all_results, file)

if __name__ == '__main__':
    theta = degrees_to_radians(60.0)
    depths = read_excel_to_points(filename = '附件.xlsx')
    depths = depth_to_numpy(depths)
    # depths = interpolate(depths, 4)

    train(depths, (5, -4.001), 10, theta)
