from turtle import *
i = 7
c = 0

# quick speed for faster debugging
speed(999999)

# position to top left corner
penup()
left(90)
forward(200)
left(90)
forward(200)
left(180)
pendown()
def create_square(endfill=0):
    global c
    if endfill == 1:
        c = 1
        forward(60)
        right(90)
        forward(60)
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

# loop to create board with squares of alternating colours
while i > 1:
    for j in range(i):
        create_square()
    right(90)
    forward(60)
    for j in range(i):
        create_square()
    right(90)
    forward(60)
    for j in range(i):
        create_square()
    right(90)
    forward(60)
    for j in range(i):
        create_square()
    right(90)
    forward(60)
    i -= 1
    print(i)
# create final square
create_square(1)

# back to original pos
penup()
right(90)
forward(120)
right(90)
forward(120)
left(90)
pendown()


input("Press enter to exit...")