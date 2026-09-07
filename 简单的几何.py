import turtle
sc=turtle.Screen()
sc.bgcolor("black")
sc.colormode(255)
t=turtle.Turtle()
t.speed(0)
t.width(2)
for i in range(300):
    r=(i*2)%255
    g=(i*3)%255
    b=(i*5)%255 
    t.pencolor(r,g,b)
    t.forward(i*1.5)
    t.left(121)
t.hideturtle()
turtle.done()