import matplotlib.pyplot as plt
from utils import *

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def line_in_grads(n, m, lines):
    for line in lines:
        vector = cross(n, m, line[0], line[1])
        if vector != []:
            line_width = 1
            plt.plot([vector[0][0],vector[1][0]], [vector[0][1],vector[1][1]], linewidth=line_width)

    # 添加图例、标签和标题
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('问题四的侧线分布图')

    # 显示图形
    plt.grid(True)
    plt.savefig('q4优解插值侧线图.png', dpi = 300)
    plt.show()

# 动画, liness是很多lines
import matplotlib.pyplot as plt
import matplotlib.animation as animation
def many_line_in_grads(n, m, liness):
    # 创建一个函数，用于生成您的plt图
    def create_plot(i):
        plt.clf()  # 清除当前图形
        line_in_grads(n, m, liness[i])
        plt.title(f'Epoch {i}')

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