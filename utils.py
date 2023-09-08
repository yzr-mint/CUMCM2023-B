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

def get_depths(length, width, center_depth, alpha, unit = 37.04):
    """
    return a list of depths, depths[x][y] means depth of (x, y)
    """
    depths = []
    # calculate the (0, 0) depth via center_depth
    o_depth = center_depth + dh(length / 2, alpha, 0)

    x_size = int(haili_to_meter(length) / unit + 1)
    y_size = int(haili_to_meter(width) / unit + 1)

    for x in range(x_size):
        depths.append([o_depth - dh(x * unit, alpha, 0) for _ in range(y_size)])

    return depths

def get_points_set(length, width, depths, theta, unit = 37.04):
    """
    return a points list

    Parameters
    ----------
    - length: haili, the length of the ocean
    - width: haili, the width of the ocean
    - depths: a list of depths(2 dimensions)
    - theta: half of the detecting angle
    - unit: 1852 * 0.02 = 37.04
    """
    points = []
    x_size = int(haili_to_meter(length) / unit + 1)
    y_size = int(haili_to_meter(width) / unit + 1)

    for x in range(x_size):
        for y in range(y_size):
            points.append(point(x, y, depths[x][y] / unit, theta))

    return points, x_size, y_size

def get_points_dic(length, width, depths, theta, unit = 37.04):
    """
    return a points list

    Parameters
    ----------
    - length: haili, the length of the ocean
    - width: haili, the width of the ocean
    - depths: a list of depths(2 dimensions)
    - theta: half of the detecting angle
    - unit: 1852 * 0.02 = 37.04
    """
    points = {}
    x_size = int(haili_to_meter(length) / unit + 1)
    y_size = int(haili_to_meter(width) / unit + 1)

    for x in range(x_size):
        for y in range(y_size):
            points[(x, y)] = point(x, y, depths[x][y] / unit, theta)

    return points, x_size, y_size

def get_depth_dic(length, width, depths, theta, unit = 37.04):
    """
    return a points list

    Parameters
    ----------
    - length: haili, the length of the ocean
    - width: haili, the width of the ocean
    - depths: a list of depths(2 dimensions)
    - theta: half of the detecting angle
    - unit: 1852 * 0.02 = 37.04
    """
    points = []
    x_size = int(haili_to_meter(length) / unit + 1)
    y_size = int(haili_to_meter(width) / unit + 1)

    for x in range(x_size):
        for y in range(y_size):
            points.append({(x, y): depths[x][y] / unit})

    return points

# 对ax+by+1=0在[xl, xh) x [yl, yr)里采样整点
def get_sample_points(a, b, xl, xr, yl, yr):
    result = []
    if a == 0:
        y = (1) / (-b)
        if yl <= y and y < yr:
            for x in range(xl, xr):
                result.append((x, floor(y)))
    elif b == 0:
        x = (1) / (-a)
        if xl <= x and x < xr:
            for y in range(yl, yr):
                result.append((floor(x), y))
    elif abs(a) >= abs(b):
        for y in range(yl, yr):
            x = (b * y + 1) / (-a)
            if xl <= x and x < xr:
                result.append((floor(x), y))
    else:
        for x in range(xl, xr):
            y = (a * x + 1) / (-b)
            if yl <= y and y < yr:
                result.append((x, floor(y)))
    return result

# 寻找[points]中被ax+by+1=0探测到的点
def get_detected_points(points, a, b):
    result = set()
    for point in points:
        if point.detected(a, b):
            result.add((point.x, point.y))
    return result

# 找到形如ax+by+c=0,经过(x0,y0)这条直线的标准形式
def get_orth(a, b, x0, y0):
    c = -a * x0 - b * y0
    return a / c, b / c