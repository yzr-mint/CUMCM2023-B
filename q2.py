"""
计算覆盖宽度
"""
from numpy import *
from utils import *
import openpyxl 

theta = degrees_to_radians(60.0)
alpha = degrees_to_radians(1.5)
center_depth = 120.0   
betas = [0, 45, 90, 135, 180, 225, 270, 315]
hailis = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1]

betas = [degrees_to_radians(beta) for beta in betas]
dists = [haili_to_meter(haili) for haili in hailis]

Ws = []

for beta in betas:
    row = []
    for dist in dists:
        if beta > pi: beta = 2 * pi - beta
        alpha_prime = get_alprime(alpha, beta)
        depth = center_depth + dh(dist, alpha, beta)
        row.append(get_width(depth, theta, alpha_prime))
    Ws.append(row)

for W in Ws:
    print(W)

workbook = openpyxl.load_workbook("result2.xlsx")
# 选择工作表
worksheet = workbook.active

for i in range(len(betas)):
    for j, haili in enumerate(hailis):
        worksheet.cell(row = i + 3, column = j + 3).value = Ws[i][j]

workbook.save("result2.xlsx")