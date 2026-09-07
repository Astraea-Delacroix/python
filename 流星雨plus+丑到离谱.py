import random
import math
from math import sin, cos, pi, log
import tkinter as tk
from tkinter import messagebox

# ====================== 全局画布配置 ======================
WIDTH = 1400
HEIGHT = 900
# 爱心位置与大小
HEART_X = 220
HEART_Y = HEIGHT - 180
IMAGE_ENLARGE = 13
HEART_COLOR = "#FF99CC"
TEXT_COLOR = "#FFFFFF"  # 文字颜色

# ====================== 爱心类 ======================
def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += HEART_X
    y += HEART_Y
    return int(x), int(y)

def scatter_inside(x, y, beta=0.15):
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
    dx = ratio_x * (x - HEART_X)
    dy = ratio_y * (y - HEART_Y)
    return x - dx, y - dy

def shrink(x, y, ratio):
    force = -1 / (((x - HEART_X) ** 2 + (y - HEART_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - HEART_X)
    dy = ratio * force * (y - HEART_Y)
    return x - dx, y - dy

def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - HEART_X) ** 2 + (y - HEART_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - HEART_X) + random.randint(-1, 1)
        dy = ratio * force * (y - HEART_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        all_points = []
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=13)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

# ====================== 最初版本流星类 ======================
class Meteor:
    def __init__(self):
        self.r = random.randint(35, 75)
        self.t = random.randint(1, 3)
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, 0)
        self.speed = random.randint(4, 8)
        self.color = random.choice(['#DDA0DD', '#EE82EE', '#DA70D6', '#BA55D3', '#FF69B4', '#FF1493'])
        self.tail = []
        self.tail_color = random.choice(['#00FF00', '#00FFFF', '#FF69B4', '#FFFFFF'])

    def update(self):
        self.x += 2 * self.speed
        self.y += self.speed
        self.tail.append((self.x, self.y, random.uniform(2, 4.5)))
        if len(self.tail) > 20:
            self.tail.pop(0)
        if self.y > HEIGHT or self.x > WIDTH:
            self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, 0)
        self.speed = random.randint(4, 8)
        self.color = random.choice(['#DDA0DD', '#EE82EE', '#DA70D6', '#BA55D3', '#FF69B4', '#FF1493'])
        self.tail = []

# ====================== 主运行函数 ======================
def start_scene():
    root = tk.Tk()
    root.title("流星雨plus")
    canvas = tk.Canvas(root, bg="black", width=WIDTH, height=HEIGHT)
    canvas.pack()

    heart = Heart()
    meteors = [Meteor() for _ in range(80)]
    frame = 0

    def draw():
        nonlocal frame
        canvas.delete("all")
        for m in meteors:
            m.update()
            for tx, ty, size in m.tail:
                canvas.create_oval(tx, ty, tx+size, ty+size, fill=m.tail_color, outline="")
            canvas.create_line(m.x, m.y, m.x - m.r*2, m.y - m.r, fill=m.color, width=3)
        # 画爱心
        for x, y, size in heart.all_points[frame % heart.generate_frame]:
            canvas.create_rectangle(x, y, x+size, y+size, fill=HEART_COLOR, outline="")
        # 在爱心中间添加文字
        canvas.create_text(HEART_X, HEART_Y, text="听我说谢谢你",
                           font=("微软雅黑", 36, "bold"), fill=TEXT_COLOR)
        frame += 1
        root.after(16, draw)
    draw()
    root.mainloop()

# ====================== kfc弹窗 ======================
def love_popup():
    root = tk.Tk()
    root.title('💜')
    root.resizable(0, 0)
    w, h = 320, 110
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text='v我50，疯狂星期四', width=39, font=('宋体',13)).place(x=0, y=12)

    def ok():
        root.destroy()
        start_scene()

    def no():
        messagebox.showwarning('💜', '再给你一次机会！')

    def close():
        messagebox.showwarning('💜', '逃避是没有用的哦')

    tk.Button(root, text='好哦', width=6, height=1, command=ok).place(x=85, y=55)
    tk.Button(root, text='不要', width=6, height=1, command=no).place(x=170, y=55)
    root.protocol('WM_DELETE_WINDOW', close)
    root.mainloop()

if __name__ == "__main__":
    love_popup()