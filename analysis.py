from utils import *

# 总长度
def length_sum(lines, xsize, ysize):
    sum = 0
    for line in lines:
        sum += in_length(ysize, xsize, line[0], line[1])
    return sum    

# 覆盖率
def cover_rate(lines, points):
    all_points_num = len(points)
    for line in lines:
        for point in points:
            if point.detected_by(line):
                points.remove(point)
    rest_points_num = len(points)
    return rest_points_num / all_points_num

# 超过20%长度
def overlap_length(lines, xsize, ysize, ratio, points):
    """
    a, b: line
    ratio: 计算大于 ratio 的线段的长度
    points: 网格点集
    """
    total_length = 0
    etas = get_eta(points, lines, xsize, ysize)
    for i in range(1, len(etas)):
        a, b = lines[i][0], lines[i][1]
        line_length = in_length(xsize, ysize, a, b)
        total_length += line_length * len([eta for eta in etas[i] if eta > ratio]) / len(etas[i])
    return total_length

