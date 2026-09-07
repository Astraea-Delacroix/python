import math
from turtle import *
import colorsys as cs
tracer(20)
bgcolor('black')
h = 0.9
for i in range(2200):
    c=cs.hsv_to_rgb(h, 1, 1)
    t=i/40
    x = 16*(math.cos(t)+0.5*math.cos(7*t))
    y = 15*(math.sin(t)+0.5*math.sin(7*t))
    goto(x*12, y*12)
    color(c)
    h += 0.004
    goto(0,0)
done()