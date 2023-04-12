from turtle import *
i = 8
global c = 0
#speed(999999)
penup()
left(90)
forward(200)
left(90)
forward(200)
left(180)
pendown()
def create_square():
    c = self.c
    if c == 0:
        fillcolor("saddlebrown")
        c = 1
    else:
        fillcolor("#efceac")
        c = 0
    begin_fill()
    forward(60)
    right(90)
    forward(60)
    right(90)
    forward(60)
    right(90)
    forward(60)
    right(90)
    forward(60)
    end_fill()

while i > 1:
    for j in range(i):
        create_square()
    right(90)
    for j in range(i):
        create_square()
    right(90)
    for j in range(i):
        create_square()
    right(90)
    for j in range(i):
        create_square()
    right(90)
    i -= 1
    print(i)