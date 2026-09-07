import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 蝴蝶曲线
t = np.linspace(0, 12 * np.pi, 4000)
base_x = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin((2 * t - np.pi) / 12) ** 5)
base_y = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t) - np.sin((2 * t - np.pi) / 12) ** 5)

fig, ax = plt.subplots(figsize=(10, 10), facecolor='#050520')
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')
ax.axis('off')

# 星空背景
np.random.seed(1)
sx = np.random.uniform(-4, 4, 200)
sy = np.random.uniform(-4, 4, 200)
ax.scatter(sx, sy, color='white', s=np.random.randint(1,3,200), alpha=0.6)

# 多层发光线条
colors = ['#ff2a70','#ff5896','#ff8cb9','#ffc0cb']
lines = [ax.plot([], [], color=c, linewidth=3-i*0.6, alpha=0.9)[0] for i,c in enumerate(colors)]

# 触须
antenna1, = ax.plot([], [], color='#ff88bb', linewidth=2)
antenna2, = ax.plot([], [], color='#ff88bb', linewidth=2)

def update(frame):
    scale = 1 + 0.03 * np.sin(frame * 0.05)
    angle = frame * 0.008
    c, s = np.cos(angle), np.sin(angle)

    for i,line in enumerate(lines):
        sc = scale * (1 - i*0.008)
        xi = base_x * sc * c - base_y * sc * s
        yi = base_x * sc * s + base_y * sc * c
        line.set_data(xi, yi)

    antenna1.set_data([0, -0.22*scale], [0, 0.8*scale])
    antenna2.set_data([0, 0.22*scale], [0, 0.8*scale])
    return *lines, antenna1, antenna2

ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.tight_layout()
plt.show()