import math
from numpy import *

# °转到弧度
def degrees_to_radians(degrees):
    radians = degrees * pi / 180.0
    return radians

# 用偏离距离, 海底夹角和航行偏角计算高度变化
# 第一问的偏离距离相当于0
def dh(dl, al, be):
    return dl * cos(be) * tan(al)

# 用深度,探测半角,海底夹角(弧度)计算宽度
def get_width(d, th, al):
    return ((d * sin(th) / sin(pi/2 - th + al)) + (d * sin(th) / sin(pi/2 - th - al))) * cos(al)

# 用海底夹角和航行偏角计算alpha'(弧度)
def get_alprime(al, be):
    return arctan(tan(be) * tan(al) * cos(be))

# 用深度和探测夹角得到 要扫到海底这点所需要的 
# 与测线的水平距离
def get_radius(d, al):
    return d * tan(al)

# 海里转换成米
def haili_to_meter(haili):
    return haili * 1852

# 变成约化角度(弧度)
def diminished_angle(th):
    return arctan(tan(th) / (1 + 0.15))
