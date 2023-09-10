import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import *

""" 可视化 q4 海床"""

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

depths = -np.array(read_excel_to_points())
m, n = depths.shape
x, y = np.mgrid[:m, :n]
points = np.column_stack((x.ravel(), y.ravel(), depths.ravel()))

# 绘制三维散点图
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c = points[:, 2], s = 1, cmap = 'cool')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('depth')

cbar = plt.colorbar(ax.scatter(points[:, 0], points[:, 1], points[:, 2], c = points[:, 2], s = 1, cmap = 'cool'))
cbar.set_label('Depth')

# plt.savefig('seabed.png', dpi = 800)
plt.show()
