from utils import *
from q3 import *
from draw_result import *
from analysis_q4 import *
import pickle

# 超过20%长度
def overlap_length(etas, lines, xsize, ysize, ratio = 0.2):
    """
    a, b: line
    ratio: 计算大于 ratio 的线段的长度
    points: 网格点集
    """
    total_length = 0.0
    for i in range(1, len(etas)):
        a, b = lines[i][0], lines[i][1]
        line_length = in_length(xsize, ysize, a, b)
        temp = line_length * len([eta for eta in etas[i] if eta > ratio]) / len(etas[i])
        total_length += temp
    return total_length


def iteration(points, lines, xsize, ysize, dir, gamma, ratio = 0.2):
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
    
    etas = get_eta(points, new_lines, xsize, ysize)
    overlap_len = overlap_length(etas, new_lines, xsize, ysize, ratio)
    print(overlap_len)
    return new_lines, overlap_len, etas


def train(depths, guide_ab, epoch, theta, inte_time = 0, unit = UNIT):
    # depth 是一个numpy矩阵, guide_ab是guide的方向, epoch是训练次数
    xsize = depths.shape[0]
    ysize = depths.shape[1]
    guide = get_nor(guide_ab[0], guide_ab[1], xsize/2, ysize/2)
    points = depth_to_point_set(depths, theta)

    theta_prime = diminished_angle(theta)
    lines = get_lines(guide, depths, theta_prime)
    all_results = []
    gamma = 40    # 插值 2
    # gamma = 10  # 未插值的 gamma，
    cooling_rate = 0.8
    print("gamma = ", gamma)
    print(len(lines))

    ratio = 0.2
    overlap_lens = []
    all_etas = []
    i = 0
    # for i in range(epoch):
    while gamma > 0.05:
        print("epoch %d" % i)
        print("gamma = ", gamma)
        i += 1
        if(i%10==0):
            with open('my_list_inte_best' + str(i) +'.pkl', 'wb') as file:
                pickle.dump(all_results, file)

            with open('my_etas_inte_best.pkl' + str(i) +'.pkl', 'wb') as file:
                pickle.dump(all_etas, file)

        lines, overlap_len, etas = iteration(points, lines, xsize, ysize, 1, gamma)
        print("number of lines: %d" % len(lines))
        all_results.append(lines)
        overlap_lens.append(overlap_len)
        all_etas.append(etas)

        lines, overlap_len, etas  = iteration(points, lines[::-1], xsize, ysize, -1, gamma)
        print("number of lines: %d" % len(lines))
        all_results.append(lines)
        overlap_lens.append(overlap_len)
        all_etas.append(etas)
        gamma *= cooling_rate

    # many_line_in_grads(xsize, ysize, all_results) # 查看训练动态变化图
    line_in_grads(ysize, xsize, all_results[-1])    # 查看最后的侧线分布图

    # 将列表保存为二进制文件，方便 analysis
    with open('my_list_inte_best.pkl', 'wb') as file:
        pickle.dump(all_results, file)

    with open('my_etas_inte_best.pkl', 'wb') as file:
        pickle.dump(all_etas, file)

    # 统计超过重叠率ratio的长度 
    visualize_train_result(overlap_lens, '最佳方向上的插值重叠率超过' + str(ratio) + '的总长度')
    final_overlap_len = overlap_lens[-1]
    print("优解插值超过重叠率" + str(ratio) + "的总长度: ", final_overlap_len * unit / inte_time)


if __name__ == '__main__':
    theta  = degrees_to_radians(60.0)
    depths = read_excel_to_points(filename = '附件.xlsx')
    depths = depth_to_numpy(depths)
    inte_time = 1

    depths = interpolate(depths, inte_time)

    train(depths, (5, 4.001), 10, theta, inte_time)
