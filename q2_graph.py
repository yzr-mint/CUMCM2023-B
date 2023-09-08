import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

# 输入数据
x_values = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1]
y_values = [0, 45, 90, 135, 180, 225, 270, 315]

# 将测量数据转换为矩阵
data = np.array([
    [415.6921938, 466.091055, 516.4899161, 566.8887772, 617.2876384, 667.6864995, 718.0853607, 768.4842218],
    [416.1201958, 451.794265, 487.4683341, 523.1424033, 558.8164725, 594.4905417, 630.1646108, 665.83868],
    [416.54908, 416.54908, 416.54908, 416.54908, 416.54908, 416.54908, 416.54908, 416.54908],
    [416.1201958, 380.4461266, 344.7720574, 309.0979883, 273.4239191, 237.7498499, 202.0757807, 166.4017116],
    [415.6921938, 365.2933327, 314.8944715, 264.4956104, 214.0967492, 163.6978881, 113.299027, 62.90016582],
    [416.1201958, 380.4461266, 344.7720574, 309.0979883, 273.4239191, 237.7498499, 202.0757807, 166.4017116],
    [416.54908, 416.54908, 416.54908, 416.54908, 416.54908, 416.54908, 416.54908, 416.54908],
    [416.1201958, 451.794265, 487.4683341, 523.1424033, 558.8164725, 594.4905417, 630.1646108, 665.83868]
])

# 创建立体图像
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 创建网格
X, Y = np.meshgrid(x_values, y_values)

# 绘制三维柱状图
ax.bar3d(X.ravel(), Y.ravel(), np.zeros_like(data).ravel(), 0.1, 0.1, data.ravel(), shade=True)

# 添加标签和标题
ax.set_xlabel('d/海里', fontproperties=font)
ax.set_ylabel('测线方向夹角/°', fontproperties=font)
ax.set_zlabel('覆盖宽度/m', fontproperties=font)
plt.title('覆盖宽度与测量参数的三维柱状图', fontproperties=font)

# 显示图像
plt.show()

