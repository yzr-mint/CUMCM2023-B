import matplotlib.pyplot as plt
import numpy as np

# 计算一个一般式直线与线段的交点
def cross_point(x0, y0, x1, y1, a, b):
    u = x0 * a + y0 * b + 1
    v = x1 * a + y1 * b + 1
    if u * v < 0:
        x = (abs(v) * x0 + abs(u) * x1) / (abs(u) + abs(v))
        y = (abs(v) * y0 + abs(u) * y1) / (abs(u) + abs(v))
        return (x, y)
    else:
        return ()

# 计算一个一般式直线ax+by+1=0与一个靠xy正半轴的, 边长为(n, m)的长方形的交点
# |n _m
def cross(n, m, a, b):
    result = []
    vertex = [(0,0),(0,n),(n,m),(m,0),(0,0)]
    for i in range(4):
        point = cross_point(vertex[i][0], vertex[i][1], vertex[i+1][0], vertex[i+1][1], a, b)
        if point != ():
            result.append(point)
    if len(result) == 1: result = []
    return result

def line_in_grads(n, m, lines):
    # 假设你有点的坐标列表，例如 [(x1, y1), (x2, y2), ...]
    points = [(x, y) for y in range(n+1) for x in range(m+1)]

    # 创建一个图形窗口
    plt.figure(figsize=(8, 8))

    # 将点的坐标分别提取出来
    x_points, y_points = zip(*points)

    # 调整节点的大小
    point_size = 3  # 设置节点的大小
    plt.scatter(x_points, y_points, s=point_size, color='blue', marker='o', label='Points')

    # 计算线的端点坐标
    for line in lines:
        vector = cross(n, m, line[0], line[1])
        if vector != []:
            line_width = 3
            plt.plot([vector[0][0],vector[1][0]], [vector[0][1],vector[1][1]], linewidth=line_width)

    # 添加图例、标签和标题
    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot and Lines')

    # 显示图形
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    line_in_grads(10, 10, [[-1,7], [2,-6]])