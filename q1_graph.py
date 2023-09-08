import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置字体以支持中文字符
font = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc', size=12)

# 创建一个包含数据的DataFrame
data = {
    '测线距中心点处的距离/m': [-800, -600, -400, -200, 0, 200, 400, 600, 800],
    '海水深度/m': [90.94873726, 85.71155294, 80.47436863, 75.23718431, 70, 64.76281569, 59.52563137, 54.28844706, 49.05126274],
    '覆盖宽度/m': [315.9215867, 297.7295851, 279.5375834, 261.3455818, 243.1535801, 224.9615785, 206.7695768, 188.5775752, 170.3855735],
    '与前一条测线的重叠率/%': [None, 0.328249492, 0.2845327, 0.234729745, 0.177474583, 0.110959296, 0.032739714, -0.060571491, -0.173808298]
}

df = pd.DataFrame(data)

# 创建柱状图
plt.figure(figsize=(10, 5))
plt.bar(df['测线距中心点处的距离/m'], df['海水深度/m'], width=40, label='海水深度')
plt.xlabel('测线距中心点处的距离/m', fontproperties=font)
plt.ylabel('海水深度/m', fontproperties=font)
plt.legend(prop=font)

plt.figure(figsize=(10, 5))
plt.bar(df['测线距中心点处的距离/m'], df['覆盖宽度/m'], width=40, label='覆盖宽度')
plt.xlabel('测线距中心点处的距离/m', fontproperties=font)
plt.ylabel('覆盖宽度/m', fontproperties=font)
plt.legend(prop=font)

plt.figure(figsize=(10, 5))
plt.bar(df['测线距中心点处的距离/m'], df['与前一条测线的重叠率/%'], width=40, label='与前一条测线的重叠率')
plt.xlabel('测线距中心点处的距离/m', fontproperties=font)
plt.ylabel('与前一条测线的重叠率/%', fontproperties=font)
plt.legend(prop=font)

plt.show()

