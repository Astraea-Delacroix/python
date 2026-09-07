import numpy as np
import matplotlib.pyplot as plt

# 创建画布，设置尺寸
fig = plt.figure(figsize=(8, 6))
# 添加3D绘图子图
ax = fig.add_subplot(111, projection='3d')

# 生成x、y轴的线性空间数据（-5到5，各100个点）
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
# 生成网格矩阵，方便计算每个点的Z值
X, Y = np.meshgrid(x, y)

# 核心：计算墨西哥草帽函数
# 加1e-6是为了避免分母为0的除零错误
Z = np.sin(np.sqrt(X**2 + Y**2) + 1e-6) / (np.sqrt(X**2 + Y**2) + 1e-6)

# 绘制3D曲面
surf = ax.plot_surface(
    X, Y, Z, 
    cmap='coolwarm',  # 配色方案：蓝到红渐变
    alpha=0.8,        # 透明度
    linewidth=0,      # 隐藏网格线
    antialiased=True  # 开启抗锯齿
)

# 隐藏坐标轴和网格，让画面更干净
ax.set_axis_off()
ax.grid(False)

# 显示图形
plt.show()