import matplotlib.pyplot as plt
import numpy as np

# 假设你有点的坐标列表，例如 [(x1, y1), (x2, y2), ...]
points = [(1, 2), (3, 4), (5, 6)]

# 假设你有线的一般式方程列表，例如 [(A1, B1, C1), (A2, B2, C2), ...]
lines = [(1, -1, 0), (-2, 3, 5), (0, 1, -3)]  # 包括一个B=0的线

# 创建一个图形窗口
plt.figure(figsize=(8, 8))

# 将点的坐标分别提取出来
x_points, y_points = zip(*points)

# 调整节点的大小
point_size = 100  # 设置节点的大小
plt.scatter(x_points, y_points, s=point_size, color='blue', marker='o', label='Points')

# 计算线的端点坐标
x_min, x_max = plt.xlim()
for line in lines:
    A, B, C = line
    if B != 0:
        x_values = np.linspace(x_min, x_max, 100)  # 生成一些 x 值用于绘制线
        y_values = (-A * x_values - C) / B
        
        # 调整线的粗细
        line_width = 2.0  # 设置线的粗细
        plt.plot(x_values, y_values, linewidth=line_width, label=f'Line {A}x + {B}y + {C} = 0')
    else:
        # 处理斜率为0的情况，绘制垂直于x轴的竖直线
        x = -C / A
        plt.vlines(x, ymin=plt.ylim()[0], ymax=plt.ylim()[1], colors='red', linestyles='dashed', linewidth=line_width, label=f'Line {A}x + {B}y + {C} = 0 (Vertical)')

# 添加图例、标签和标题
plt.legend()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot and Lines')

# 显示图形
plt.grid(True)
plt.show()

