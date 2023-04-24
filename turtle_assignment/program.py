from turtle import *

# setting
setup(800, 800)
window = Screen()
window.title("Checkers Assignment")
window.bgcolor("darkslateblue")

i = 7  # square iterator
c = 0  # colour iterator
board = []  # board array

for i in range(8):
    board.append([])
    for j in range(8):
        board[i].append(0)

# quick speed for faster debugging
#speed(0)
tracer(0, 0)

# position to top left corner
penup()
left(90)
forward(200)
left(90)
forward(200)
left(180)
pendown()

# function to create a square


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

# create circle from top right corner of square


def create_circle(colour):
    if colour == "white":
        fillcolor("#e9ce9b")
        pencolor("#d2b26d")
    else:
        fillcolor("#000000")
        pencolor("#8c510a")
    forward(5)
    right(90)
    forward(30)
    pendown()
    begin_fill()
    circle(25)
    penup()
    left(90)
    forward(5)
    right(90)
    pendown()
    circle(20)
    end_fill()
    penup()
    back(30)
    left(90)
    back(10)


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
right(90)
# create_circle("white")

# use board array to put pieces in correct positions
for y in range(8):
    for x in range(8):
        if (y + x) % 2 != 0:
            forward(60*x)
            right(90)
            forward(60*y)
            left(90)
            if y < 3:
                create_circle("white")
            elif y > 4:
                create_circle("black")
            # return to original pos
            back(60*x)
            right(90)
            back(60*y)
            left(90)

input("Press enter to exit...")


# 0 [[0, 1, 0, 3, 0, 5, 0, 7],
#1 [0, 0, 2, 0, 4, 0, 6, 0],
#2 [0, 0, 0, 0, 0, 0, 0, 0],
#3 [0, 0, 0, 0, 0, 0, 0, 0],
#4 [0, 0, 0, 0, 0, 0, 0, 0],
#5 [0, 0, 0, 0, 0, 0, 0, 0],
#6 [0, 0, 0, 0, 0, 0, 0, 0],
# 7 [0, 0, 0, 0, 0, 0, 0, 0]]


# 0, 1 true
# 0, 3 true
# 0, 5 true
# 0, 7 true
# 1, 0 true
# 1, 2 true
# 1, 4 true
# 1, 6 true
# 2, 1 true
# 2, 3 true
# 2, 5 true
# 2, 7 true