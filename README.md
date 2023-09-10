# README:
problem: B
## 安装
``` shell
pip install numpy
pip install openpyxl
pip install matplotlib
pip install pandas
pip install pickle
```

## 功能
- `q1.py`: 解决问题一，并填写到 `result1.xlsx`
- `q1_graph.py`: 可视化问题一
- `q2.py`: 解决问题二，并填写到 `result2.xlsx`
- `q2_graph.py`: 可视化问题二
- `q3.py`: 解决问题三
- `analysis_q3.py`: 分析问题三并提供指标参数
- `q4.py`: 解决问题四
- `analysis_q4.py`: 分析问题四并提供指标参数
- `draw_results.py`: 可视化问题三、四的测线分布，并生成动图
- `drawseabed.py`:可视化问题三、四的海床
- `utils`: 工具库

## 注意
- `q4.py` 运行时注意 `utils.py` 中的约化角度改为 0.2
``` py
# 变成约化角度(弧度)
# q3 设置为 0.11
# q4 设置为 0.20
def diminished_angle(th):
    return arctan((1 - 0.11)*tan(th))   # 如果你使用q4.py，你需要将0.11改为0.2
```
- `analysis_q4.py` 得到结果注意单位