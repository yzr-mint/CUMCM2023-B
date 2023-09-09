from numpy import *
import openpyxl

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


# 对ax+by+1=0在[xl, xh) x [yl, yr)里采样准确点
def get_real_points(a, b, xl, xr, yl, yr):
    result = []
    if a == 0:
        y = (1) / (-b)
        if yl <= y and y < yr:
            for x in range(xl, xr):
                result.append((x, y))
    elif b == 0:
        x = (1) / (-a)
        if xl <= x and x < xr:
            for y in range(yl, yr):
                result.append((x, y))
    elif abs(a) >= abs(b):
        for y in range(yl, yr):
            x = (b * y + 1) / (-a)
            if xl <= x and x < xr:
                result.append((x, y))
    else:
        for x in range(xl, xr):
            y = (a * x + 1) / (-b)
            if yl <= y and y < yr:
                result.append((x, y))
    return result

# 寻找[points]中被ax+by+1=0探测到的点
def get_detected_points(points, a, b):
    result = set()
    for point in points:
        if point.detected_by(a, b):
            result.add((point.x, point.y))
    return result

# 找到形如ax+by+c=0,经过(x0,y0)这条直线的标准形式
def get_nor(a, b, x0, y0):
    c = -a * x0 - b * y0
    return a / c, b / c

# 将放缩之后的直线的方程转化为原来以米为单位的讨论上
def get_origin_param(a, b, unit = UNIT): 
    return a / unit, b / unit


# 返回重叠率（相对于前一条线）
def get_eta(points, lines, xsize, ysize):
    etas = [0]
    for i, (Aa, Ab) in enumerate(lines[1:]):
        # get dots on the line
        dots = get_real_points(Aa, Ab, 0, xsize, 0, ysize)
        eta_in_A = []
        Ba, Bb = lines[i]
        A_dots = get_detected_points(points, Aa, Ab)
        B_dots = get_detected_points(points, Ba, Bb)
        for (x, y) in dots:
            # get points on the grid inside dot detection range
            la, lb = -Ab / (Ab * x - Aa * y), Aa / (Ab * x - Aa * y)
            line_dots = get_sample_points(la, lb, 0, xsize, 0, ysize)
            overlap = set(A_dots) & set(B_dots) & set(line_dots)
            if len(overlap): # eta > 0
                eta_in_A.append(len(overlap) / len(set(A_dots) & set(line_dots)))
            else:            # eta < 0
                insect_Bx = int((Bb - lb) / (lb * Ba - la * Bb))
                insect_By = int((la - Ba) / (lb * Ba - la * Bb))
                temp_line = get_sample_points(la, lb, 
                                              min(insect_Bx, int(x)), 
                                              max(insect_Bx, int(x)), 
                                              min(insect_By, int(y)), 
                                              max(insect_By, int(y)))
                points_not_overlap = [d for d in temp_line if d not in A_dots and d not in B_dots]
                eta_in_A.append(-len(points_not_overlap) / len(set(A_dots) & set(line_dots)))
        etas.append(eta_in_A)
    return etas

# 第四问读取表格，返回点集合(已经除以unit)
def read_excel_to_points(filename = '附件.xlsx', theta = degrees_to_radians(60), 
                         start_x = 3, start_y = 3, 
                         xsize = 200, ysize = 250, unit = UNIT):
    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook.active

    depths = []
    for i in range(xsize):
        rows = []
        for j in range(ysize):
            rows.append(worksheet.cell(row = j + start_y, column = i + start_x).value / unit)
        depths.append(rows)

    return depths

# 返回斜率
def get_k(a, b):
    return - a / b

# 返回加权和
def weight_sum(lst, center = 0.15):
    size = len(lst)
    weights = linspace(0, 1, size)  # 使用np.linspace生成等间隔的权重数组
    result = sum(array(lst) * weights)
    return result - center

# 得到沿着x轴方向（即东西方向）的线与所提供直线的交点坐标
def get_point_with_x(a, b, fix_x):
    return fix_x, (-1 - a * fix_x) / b

# 得到沿着y轴方向（即南北方向）的线与所提供直线的交点坐标
def get_point_with_y(a, b, fix_y):
    return (-1 - b * fix_y), fix_y