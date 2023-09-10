from utils import *
import matplotlib.pyplot as plt
import pickle

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def length_sum(lines, xsize, ysize):
    """ 返回在矩形海域内的侧线总长度 """
    return len(lines) * ysize * UNIT


def cover_rate(lines, points):
    """ 返回侧线在矩形海域网格点的覆盖率 """
    all_points_num = len(points)
    for line in lines:
        S = set()
        for point in points:
            if point.detected_by(line[0], line[1]):
                S.add(point)
        for s in S:
            points.remove(s)
    rest_points_num = len(points)
    return 1 - rest_points_num / all_points_num


def get_eta_for_q3(center_depth, alpha, theta, lines, xsize, inte_time, unit = UNIT):
    """ 这里的center_depth是米 返回q3的eta"""
    # 得到宽度 W
    unit /= 2 ** (inte_time)
    xsize *= 2 ** (inte_time)
    W = 0.0
    depths = []
    o_depth = center_depth / unit + dh(xsize / 2, alpha, 0)
    depths = [o_depth - dh(-10000 / a, alpha, 0) for (a, b) in lines]
    for d in depths[1:]:
        W += get_width(d, theta, alpha)
    return (W - xsize) / W

if __name__ == '__main__':
    theta = degrees_to_radians(60.0)
    alpha = degrees_to_radians(1.5)
    xsize = 200
    ysize = 100

    inte_time = 5
    depths = get_depths(4, 2, 110, alpha)
    points = depth_to_point_set(depths, theta)

    with open('result3.pkl', 'rb') as f:
        data = pickle.load(f)
    print(len(data))
    print("eta: ", get_eta_for_q3(110, alpha, theta, data, xsize, inte_time))
    print("sum of line length: ", length_sum(data, xsize, ysize))
    print(cover_rate(data, points))
    # print(-10000 / 2 ** (inte_time) / array(data)[:, 0]) # 转化为 x 坐标