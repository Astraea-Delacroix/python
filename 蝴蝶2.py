import turtle
import math

# 窗口配置
win = turtle.Screen()
win.setup(800, 800)
win.bgcolor('#050520')
win.title("动态蝴蝶")
win.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# 蝴蝶曲线，放大系数25
def draw_butterfly(scale):
    pen.penup()
    for i in range(0, 360*12, 2):
        t = math.radians(i)
        x = scale * math.sin(t) * (math.exp(math.cos(t)) - 2*math.cos(4*t) - math.sin((2*t - math.pi)/12)**5)
        y = scale * math.cos(t) * (math.exp(math.cos(t)) - 2*math.cos(4*t) - math.sin((2*t - math.pi)/12)**5)
        pen.goto(x, y)
        pen.pendown()
    pen.pencolor("#ff5896")

# 安全动画循环
def animate():
    for s in [25, 26, 25, 24]:
        pen.clear()
        draw_butterfly(s)
        win.update()
    win.ontimer(animate, 100)

animate()
turtle.done()