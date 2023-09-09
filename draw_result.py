import matplotlib.pyplot as plt
from utils import *

def line_in_grads(n, m, lines):
    # 假设你有点的坐标列表，例如 [(x1, y1), (x2, y2), ...]
    points = [(x, y) for y in range(n+1) for x in range(m+1)]

    # 创建一个图形窗口
    #plt.figure(figsize=(50,50))

    # 将点的坐标分别提取出来
    x_points, y_points = zip(*points)

    # 调整节点的大小
    point_size = 3  # 设置节点的大小
    #plt.scatter(x_points, y_points, s=point_size, color='blue', marker='o', label='Points')

    # 计算线的端点坐标
    for line in lines:
        vector = cross(n, m, line[0], line[1])
        if vector != []:
            line_width = 1
            plt.plot([vector[0][0],vector[1][0]], [vector[0][1],vector[1][1]], linewidth=line_width)

    # 添加图例、标签和标题
    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot and Lines')

    # 显示图形
    plt.grid(True)
    plt.show()

# 动画, liness是很多lines
import matplotlib.pyplot as plt
import matplotlib.animation as animation
def many_line_in_grads(n, m, liness):
    # 创建一个函数，用于生成您的plt图
    def create_plot(i):
        plt.clf()  # 清除当前图形
        line_in_grads(n, m, liness[i])

    # 设置动画参数
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, create_plot, frames=len(liness), interval=1000)

    # 保存动画为文件或显示在窗口中
    # 若要保存为文件，可以使用下面的代码：
    # ani.save('my_animation.gif', writer='pillow')

    # 若要在窗口中显示动画，可以使用下面的代码：
    plt.show()

if __name__ == "__main__":
    line_in_grads(200, 250, [[-0.05,7], [3,-0.06]])
    many_line_in_grads(200, 250, [[[-0.05,7], [3,-0.06]], [[-0.05,0.04], [0.033,-0.06]]])