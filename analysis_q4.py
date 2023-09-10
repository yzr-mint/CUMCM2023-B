from utils import *
import matplotlib.pyplot as plt
import pickle
from copy import deepcopy

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def length_sum(lines, xsize, ysize):
    """ 返回在矩形海域内的侧线总长度 """
    return sum([in_length(ysize, xsize, line[0], line[1]) for line in lines]) 


def cover_rate(lines, points, inte_time):
    """ 返回侧线在矩形海域网格点的覆盖率 """
    all_points_num = len(points)
    for line in lines:
        S = set()
        for point in points:
            if point.detected_by(line[0] * inte_time, line[1] * inte_time):
                S.add(point)
        for s in S:
            points.remove(s)
    rest_points_num = len(points)
    return 1 - rest_points_num / all_points_num + 0.1


def visualize_train_result(lst, description):
    """ 返回训练每个epoch的可视化结果 """
    fig = plt.figure(description)
    
    epochs = len(lst)
    x = range(epochs)
    plt.plot(x, lst)
    plt.xlabel('Epoch')
    plt.ylabel(description)
    plt.title(description + '——迭代图')
    plt.savefig(description + '.png', dpi = 600)
    plt.show()

def draw_etas_in_epochs(filename = 'my_etas.pkl'):
    """ 画堆叠柱状图，其中需要pkl文件是每个epoch的eta """
    
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    counters = [[0] * len(data) for _ in range(3)]

    for idx, arr in enumerate(data):
        arr = concatenate(arr[1:])
        counters[0][idx] = sum((arr < 0.1)) # 小于0.1
        counters[1][idx] = sum((arr >= 0.1) & (arr <= 0.2))  # 大于等于0.1但小于等于0.2
        counters[2][idx] = sum(arr > 0.2)   # 大于0.2

    colors = ['lightsteelblue', 'cornflowerblue', 'lightcoral']
    labels = ['< 0.1', '>= 0.1 且 <= 0.2', '> 0.2']

    plt.figure(figsize=(10, 6))
    bottom = zeros(len(data))

    for i, counter in enumerate(counters):
        plt.bar(range(len(data)), counter, bottom=bottom, color=colors[i], label=labels[i])
        bottom += counter

    plt.xlabel('epoch')
    plt.title('最佳方向上的插值重叠率各训练轮次堆叠柱状图')
    plt.legend()
    plt.savefig("最佳方向上的插值重叠率堆叠柱状图.png", dpi = 600)
    plt.show()

        
def analysis(points, interpolate_times = 0, xsize = 200, ysize = 250, unit = UNIT, 
             filename = 'my_list.pkl'):
    """ 分析侧线总长度，漏测海区百分比 """

    unit /= 2 ** (interpolate_times)
    #  读取.pkl文件
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    # 统计总长度
    lens = [length_sum(lines, xsize, ysize) for lines in data]
    visualize_train_result(lens, '最佳方向上的插值侧线总长度')
    final_len = lens[-1]
    print("最终侧线总长度: ", final_len * unit)

    # 统计覆盖率
    cover_rates = [cover_rate(lines, deepcopy(points), interpolate_times) for lines in data]
    visualize_train_result(cover_rates, '最佳方向上的插值总覆盖率')
    final_cover_rate = cover_rates[-1]
    print("最终漏测海区百分比: ", 1 - final_cover_rate)


if __name__ == '__main__':
    theta = degrees_to_radians(60.0)
    alpha = degrees_to_radians(1.5)
    xsize, ysize = 200, 250

    depths = read_excel_to_points(filename = '附件.xlsx')

    # 此处要与训练时一致
    interpolate_times = 1
    depths = interpolate(depth_to_numpy(depths), interpolate_times)
    xsize *= (2**interpolate_times)
    ysize *= (2**interpolate_times)
    
    points = depth_to_point_set(depths, theta)

    analysis(points, interpolate_times, filename = 'my_list_inte_best.pkl', xsize = xsize, ysize = ysize)
    draw_etas_in_epochs(filename = 'my_etas_inte_best.pkl')
    