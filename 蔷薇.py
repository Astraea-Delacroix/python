import turtle
import random

# 基础画布设置
t = turtle.Turtle()
turtle.setup(800, 800)
turtle.bgcolor("#000000")  # 黑色背景还原视频深色效果
t.speed(0)
turtle.tracer(0)  # 关闭动画卡顿，实现流畅动态

# 主色：冰晶蓝
main_color = "#00ccff"
light_color = "#66e5ff"
dark_color = "#0066cc"

# ---------------------- 核心：for循环绘制花瓣 ----------------------
def draw_petal(x, y, size, angle):
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.pendown()
    t.color(main_color, light_color)
    t.begin_fill()
    # for循环勾勒花瓣轮廓
    for _ in range(2):
        t.circle(size, 60)
        t.left(120)
        t.circle(size, 60)
        t.left(120)
    t.end_fill()

# 绘制整朵蔷薇（嵌套for循环）
def draw_rose():
    # 外层花瓣
    for i in range(8):
        # if判断：奇偶花瓣大小/颜色区分，实现层次
        if i % 2 == 0:
            draw_petal(0, 0, 120, i * 45)
        else:
            draw_petal(0, 0, 90, i * 45 + 22)
    # 内层花瓣
    for i in range(6):
        if i % 2 == 0:
            draw_petal(0, 0, 60, i * 60 + 30)
        else:
            draw_petal(0, 0, 40, i * 60)
    # 花蕊
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.dot(30, "#0099ff")

# ---------------------- 动态水滴（for+if实现下落） ----------------------
drops = []
# 初始化水滴
for _ in range(12):
    drops.append({
        "x": random.randint(-80, 80),
        "y": random.randint(-100, -30),
        "speed": random.randint(3, 6)
    })

def draw_drops():
    t.clear()
    draw_rose()
    # for循环遍历所有水滴
    for drop in drops:
        t.penup()
        t.goto(drop["x"], drop["y"])
        t.pendown()
        t.color(light_color)
        t.dot(8)
        # if判断：水滴下落，超出边界重置位置（守护花期，循环存续）
        drop["y"] -= drop["speed"]
        if drop["y"] < -400:
            drop["y"] = random.randint(-100, -30)
            drop["x"] = random.randint(-80, 80)
    turtle.update()
    turtle.ontimer(draw_drops, 30)

# 启动
draw_drops()
turtle.done()