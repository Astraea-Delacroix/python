import numpy as np
import matplotlib.pyplot as plt
# 创建画布，设置尺寸
fig = plt.figure(figsize=(8, 6))
# 添加3D绘图子图
ax = fig.add_subplot(111, projection='3d')
# 心形的2D参数方程（来自经典的心形线公式）
t = np.linspace(0, 2 * np.pi, 100)
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
# 生成z轴的线性空间数据，用于拉伸成3D
z = np.linspace(-5, 5, 100)
# 构建网格矩阵
X, Z = np.meshgrid(x, z)
Y, _ = np.meshgrid(y, z)
# 绘制3D曲面，使用Reds配色，模拟渐变爱心
ax.plot_surface(
    X, 
    np.tile(y, (100, 1)),  # 将y轴数据沿z轴方向重复100次
    Z, 
    cmap='Reds', 
    alpha=0.9  # 透明度
)
# 隐藏坐标轴，让画面更干净
ax.set_axis_off()
# 显示图形
plt.show()