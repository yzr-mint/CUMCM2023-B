from numpy import *

UNIT = 37.04

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
def get_radius(d, th):
    return d * tan(th)

# 海里转换成米
def haili_to_meter(haili):
    return haili * 1852

# 变成约化角度(弧度)
def diminished_angle(th):
    return arctan(tan(th) / (1 + 0.15))

# 把两点式化成标准形式ax+by+1=0
def normalize(x1, y1, x2, y2):
    return (y2-y1)/(x2*y1-x1*y2), (x1-x2)/(x2*y1-x1*y2)


# 海底点的类
class point:
    def __init__(self, x, y, z, theta):
        self.x = x
        self.y = y
        self.z = z
        # 是半径的平方!
        self.r2 = (z * tan(theta))**2
    
    # 直线统一用ax+by+1=0
    def detected_by(self, a, b):
        return self.r2 * (a ** 2 + b ** 2) > (a*self.x + b*self.y + 1) ** 2
    
    # 看(x,y)是不是在半径范围内
    def close_enough(self, x, y):
        return (self.x - x)**2 + (self.y - y)**2 < self.r2

def get_depths(length, width, center_depth, alpha, unit = UNIT):
    """
    return a list of depths, depths[x][y] means depth of (x, y)
    """
    depths = []
    # calculate the (0, 0) depth via center_depth
    o_depth = center_depth + dh(haili_to_meter(length) / 2, alpha, 0)

    x_size = int(haili_to_meter(length) / unit + 1)
    y_size = int(haili_to_meter(width) / unit + 1)

    for x in range(x_size):
        depths.append([(o_depth - dh(x * unit, alpha, 0)) / unit for _ in range(y_size)])

    return depths

def depth_to_point_dic(depth, theta):
    xsize = len(depth)
    ysize = len(depth[0])
    # 假设你已经有了二维数组d和x_size、y_size的值
    return {(x, y): point(x, y, depth[x][y], theta) for x in range(xsize) for y in range(ysize)}, xsize, ysize

def depth_to_point_set(depth, theta):
    xsize = len(depth)
    ysize = len(depth[0])
    # 假设你已经有了二维数组d和x_size、y_size的值
    return {point(x, y, depth[x][y], theta) for x in range(xsize) for y in range(ysize)}

def depth_to_depth_dic(depth):
    return {dep for i in depth for dep in i}

def depth_to_numpy(depth):
    return array(depth)

def interpolate(d_matrix, times):
    for i in range(times):
        # 计算相邻两行的平均值
        row_avg = (d_matrix[:-1] + d_matrix[1:]) / 2
        # 将平均值插入到相邻两行之间
        tmp1 = vstack((d_matrix, row_avg))
        # 计算相邻两列的平均值
        col_avg = (tmp1[:, :-1] + tmp1[:, 1:]) / 2
        # 将平均值插入到相邻两列之间
        tmp2 = hstack((tmp1, col_avg))
        # 把高度按比例增加
        d_matrix = tmp2 * 2
    return d_matrix


    

# 对ax+by+1=0在[xl, xh) x [yl, yr)里采样整点
def get_sample_points(a, b, xl, xr, yl, yr):
    result = []
    if a == 0:
        y = (1) / (-b)
        if yl <= y and y < yr:
            for x in range(xl, xr):
                result.append((x, int(floor(y))))
    elif b == 0:
        x = (1) / (-a)
        if xl <= x and x < xr:
            for y in range(yl, yr):
                result.append((int(floor(x)), y))
    elif abs(a) >= abs(b):
        for y in range(yl, yr):
            x = (b * y + 1) / (-a)
            if xl <= x and x < xr:
                result.append((int(floor(x)), y))
    else:
        for x in range(xl, xr):
            y = (a * x + 1) / (-b)
            if yl <= y and y < yr:
                result.append((x, int(floor(y))))
    return result

# 寻找[points]中被ax+by+1=0探测到的点
def get_detected_points(points, a, b):
    result = set()
    for point in points:
        if point.detected_by(a, b):
            result.add((point.x, point.y))
    return result

# 找到形如ax+by+c=0,经过(x0,y0)这条直线的标准形式
def get_orth(a, b, x0, y0):
    c = -a * x0 - b * y0
    return a / c, b / c

# 将放缩之后的直线的方程转化为原来以米为单位的讨论上
def get_origin_param(a, b, unit = UNIT): 
    return a / unit, b / unit


