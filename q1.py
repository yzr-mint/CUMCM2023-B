"""
计算海水深度，覆盖宽度和重叠率
"""
from numpy import *
from utils import *
import pandas as pd

theta = degrees_to_radians(60.0)
alpha = degrees_to_radians(1.5)
center_depth = 70.0     
d = 200

dists = [-800, -600, -400, -200, 0, 200, 400, 600, 800]

depths = [center_depth + dh(-dist, alpha, 0) for dist in dists]
Ws = [get_width(depths[i], theta, alpha) for i, dist in enumerate(dists)]
etas = [1 - d / W for W in Ws]
etas[0] = '--'

df = pd.read_excel('result1.xlsx')

for i, dist in enumerate(dists):
    df.at[0, dist] = depths[i]
    df.at[1, dist] = Ws[i]
    df.at[2, dist] = etas[i]

df.to_excel('result1.xlsx', index = False)
