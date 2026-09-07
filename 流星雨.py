import turtle as tu
import random as ra
import tkinter as tk
import math
from tkinter import messagebox

def Meteors():
    # 放大画布窗口
    tu.setup(width=1400, height=900)
    tu.bgcolor('black')
    tu.title("放大版·紫粉色流星雨+蓝色拖尾")
    t = tu.Pen()
    t.hideturtle()
    tu.tracer(0)
    # 流星主体：紫粉色系
    meteor_colors = ['#DDA0DD', '#EE82EE', '#DA70D6', '#BA55D3', '#FF69B4', '#FF1493']
    # 拖尾粒子：蓝色系
    tail_colors = ['#87CEFA', '#1E90FF', '#00BFFF', '#4169E1', '#00FFFF']

    class Star():
        def __init__(self):
            # 放大流星本体尺寸
            self.r = ra.randint(35, 75)
            self.t = ra.randint(1, 3)
            # 适配放大画布，扩大坐标范围
            self.x = ra.randint(-700, 700)
            self.y = ra.randint(350, 450)
            self.speed = ra.randint(4, 8)
            self.color = ra.choice(meteor_colors)
            self.outline = 1
            self.tail_particles = []

        def add_tail(self):
            # 放大拖尾粒子
            self.tail_particles.append({
                "x": self.x,
                "y": self.y,
                "size": ra.uniform(2, 4.5),
                "life": ra.randint(15, 25), # 延长拖尾长度
                "color": ra.choice(tail_colors)
            })

        def update_tail(self):
            new_tail = []
            for p in self.tail_particles:
                p["y"] += self.speed * 0.8
                p["x"] += self.speed * 1.6
                p["life"] -= 1
                p["size"] *= 0.9
                if p["life"] > 0:
                    new_tail.append(p)
            self.tail_particles = new_tail

        def draw_tail(self):
            for p in self.tail_particles:
                t.penup()
                t.goto(p["x"], p["y"])
                t.pendown()
                t.dot(p["size"], p["color"])

        def star(self):
            t.pensize(self.outline)
            t.penup()
            t.goto(self.x, self.y)
            t.pendown()
            t.color(self.color)
            t.begin_fill()
            t.fillcolor(self.color)
            t.setheading(-30)
            t.right(self.t)
            t.forward(self.r)
            t.left(self.t)
            t.circle(self.r*math.sin(math.radians(self.t)),180)
            t.left(self.t)
            t.forward(self.r)
            t.end_fill()

        def move(self):
            if self.y >= -450:
                self.y -= self.speed
                self.x += 2*self.speed
                self.add_tail()
                self.update_tail()
            else:
                self.r = ra.randint(35,75)
                self.t = ra.randint(1,3)
                self.x = ra.randint(-700,700)
                self.y = 350
                self.speed = ra.randint(4,8)
                self.color = ra.choice(meteor_colors)
                self.outline = 1
                self.tail_particles = []

    Stars = [Star() for _ in range(80)]

    while True:
        t.clear()
        for star in Stars:
            star.move()
            star.draw_tail()
            star.star()
        tu.update()

def love():
    root = tk.Tk()
    root.title('💜')
    root.resizable(0, 0)
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    widths, heights = 320, 110
    x = (screenwidth - widths) // 2
    y = (screenheight - heights) // 2
    root.geometry(f'{widths}x{heights}+{x}+{y}')
    tk.Label(root, text='v我50，疯狂星期四', width=39, font=('宋体',13)).place(x=0, y=12)

    def OK():
        root.destroy()
        Meteors()

    def NO():
        messagebox.showwarning('💜', '再给你一次机会！')

    def closeWindow():
        messagebox.showwarning('💜', '逃避是没有用的哦')

    tk.Button(root, text='好哦', width=6, height=1, command=OK).place(x=85, y=55)
    tk.Button(root, text='不要', width=6, height=1, command=NO).place(x=170, y=55)
    root.protocol('WM_DELETE_WINDOW', closeWindow)
    root.mainloop()

if __name__ == "__main__":
    love()