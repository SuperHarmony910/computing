from enum import IntEnum
import math
from turtle import Turtle, Screen, setup, tracer, mainloop

t = Turtle()

# setting
setup(0.5401041667, 0.80546875, 0.5, 0.5)
window = Screen()
window.title("Checkers Assignment")
window.bgcolor("darkslateblue")

i = 7  # square iterator
c = 0  # colour iterator
board = []  # board array
selected = [0, 0, False] # if a piece is selected or not
is_move_to = False # if a piece is selected and is moving to a square

# create a class for the pieces
class PieceType(IntEnum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    # WHITE_KING = 3
    # BLACK_KING = 4
    # WHITE_SELECTED = 5
    # BLACK_SELECTED = 6
    # WHITE_KING_SELECTED = 7
    # BLACK_KING_SELECTED = 8
    WHITE_MOVE = 3 #9
    BLACK_MOVE = 4 #10
    # WHITE_KING_MOVE = 11
    # BLACK_KING_MOVE = 12

class Piece:
    def __init__(self, x, y, type: PieceType, king = False, selected = False):
        self.x = x
        self.y = y
        self.type: PieceType = type
        self.king = king
        self.selected = selected

for i in range(8):
    board.append([])
    for j in range(8):
        board[i].append(Piece(i, j, PieceType.EMPTY))

# quick speed for faster debugging
t.speed(0)  # 0 = fastest, 1 = slowest - adjust before submission!
tracer(0, 0)  # instant drawing (no animation), very useful for debugging

# position to top t.left corner
t.penup()
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(180)
t.pendown()


# function to create a square
def create_square(endfill=0):
    global c
    if endfill == 1:
        c = 1
        t.forward(60)
        t.right(90)
        t.forward(60)
    if c == 0:
        t.fillcolor("saddlebrown")
        c = 1
    else:
        t.fillcolor("#efceac")
        c = 0
    t.begin_fill()
    t.forward(60)
    t.right(90)
    t.forward(60)
    t.right(90)
    t.forward(60)
    t.right(90)
    t.forward(60)
    t.right(90)
    t.forward(60)
    t.end_fill()


def create_piece(type):
    checker = t
    if type == "white":
        t.color("#d2b26d", "#e9ce9b")
    else:
        t.color("#1b100b", "#300c09")
    checker.pensize(3)
    checker.forward(5)
    checker.right(90)
    checker.forward(30)
    checker.pendown()
    checker.begin_fill()
    checker.circle(25)
    checker.penup()
    checker.left(90)
    checker.forward(5)
    checker.right(90)
    checker.pendown()
    checker.circle(20)
    checker.end_fill()
    checker.penup()
    checker.back(30)
    checker.left(90)
    checker.back(10)


# loop to create board with squares of alternating colours
while i > 1:
    for j in range(i):
        create_square()
    t.right(90)
    t.forward(60)
    for j in range(i):
        create_square()
    t.right(90)
    t.forward(60)
    for j in range(i):
        create_square()
    t.right(90)
    t.forward(60)
    for j in range(i):
        create_square()
    t.right(90)
    t.forward(60)
    i -= 1
    # print(i)

# create final square
create_square(1)

# back to original pos
t.penup()
t.right(90)
t.forward(120)
t.right(90)
t.forward(120)
t.right(90)

# use board array to put pieces in correct positions
for y in range(8):
    for x in range(8):
        if (y + x) % 2 != 0:
            t.forward(60*x)
            t.right(90)
            t.forward(60*y)
            t.left(90)
            if y < 3:
                board[int(round(t.pos()[1]-200)//-60)
                      ][int(round(t.pos()[0]+260)//60)].type = PieceType.WHITE
                create_piece("white")
            elif y > 4:
                board[int(round(t.pos()[1]-200)//-60)
                      ][int(round(t.pos()[0]+260)//60)].type = PieceType.BLACK
                create_piece("black")

            # return to original t.pos
            t.back(60*x)
            t.right(90)
            t.back(60*y)
            t.left(90)

# draw the coordinate of each square on the board
# this is for debugging purposes
for y in range(8):
    for x in range(8):
        t.forward(60*x)
        t.right(90)
        t.forward(60*y+30)
        t.left(90)
        t.forward(30)
        t.color('deepskyblue')
        t.write(str(x) + ", " + str(y), align="center",
                font=("Arial", 18, "normal"))
        t.color('black')
        t.back(30)
        t.back(60*x)
        t.right(90)
        t.back(60*y+30)
        t.left(90)

# make this checkers board playable
# 0 = empty, 1 = white, 2 = black
# 3 = white king, 4 = black king
# 5 = white selected, 6 = black selected
# 7 = white king selected, 8 = black king selected
# 9 = white move, 10 = black move
# 11 = white king move, 12 = black king move

# check which squares are available
def available_squares(x, y):
    available_squares = []
    # make sure coordinate is not out of bounds
    if x < 7 and y < 7:
        if x >= 0 and y >= 0:
            if board[y][x].type == PieceType.BLACK:
                if board[y-1][x+1].type == PieceType.EMPTY:
                    available_squares.append([x+1, y-1])
                if board[y-1][x-1].type == PieceType.EMPTY:
                    available_squares.append([x-1, y-1])
                # check if square is empty
                # black king: [y+1][x+1], [y-1][x+1]
                # white king: [y-1][x-1], [y+1][x-1]
                if board[y][x].king == True:
                    if board[y-1][x+1].type == PieceType.EMPTY:
                        available_squares.append([x+1, y+1])

                while board[y+1][x+1].type == PieceType.WHITE:
                    y = y + 2
                    x = x + 2
                while board[y-1][x+1].type == PieceType.WHITE:
                    y = y - 2
                    x = x + 2
                while board[y+1][x-1].type == PieceType.WHITE:
                    y = y + 2
                    x = x - 2
                while board[y-1][x-1].type == PieceType.WHITE:
                    y = y - 2
                    x = x - 2
            if board[y][x].type == PieceType.WHITE:
                print('white')
                if board[y+1][x+1].type == PieceType.EMPTY:
                    available_squares.append([x+1, y+1])
                if board[y+1][x-1].type == PieceType.EMPTY:
                    available_squares.append([x-1, y+1])
                if board[y][x].king == True:
                    if board[y-1][x+1].type == PieceType.EMPTY:
                        available_squares.append([x+1, y-1])
                    if board[y-1][x-1].type == PieceType.EMPTY:
                        available_squares.append([x-1, y-1])
                        
                while board[y+1][x+1].type == PieceType.BLACK:
                    y = y + 2
                    x = x + 2
                while board[y-1][x+1].type == PieceType.BLACK:
                    y = y - 2
                    x = x + 2
                while board[y+1][x-1].type == PieceType.BLACK:
                    y = y + 2
                    x = x - 2
                while board[y-1][x-1].type == PieceType.BLACK:
                    y = y - 2
                    x = x - 2

    print(available_squares)
    return available_squares


# get clicked coordinates
def mouse_event(xraw, yraw): # returns x, y, is_move_to
    global selected
    global is_move_to
    y = math.floor(round(yraw-200)//-60)
    x = math.floor(round(xraw+260)//60)
    if y > 7 or x > 7 or x < 0 or y < 0:
        return False  # print('out of bounds')
    
    print(x, y, board[y][x].selected)
    if selected[2] == True:
        selected[0] = False
        selected[1] = False
        selected[2] = False
        is_move_to = True
        highlight_moves(available_squares(x, y), True)
        #return x, y, True
    else:
        selected[0] = x
        selected[1] = y
        selected[2] = True
        is_move_to = False
        highlight_moves(available_squares(x, y), False)
    #return x, y, False

    try:
        board[selected[0]][selected[1]].selected = selected[2]
        print(f'available squares: {available_squares(x, y)}')
    except:
        board[selected[0]][selected[1]] = Piece(selected[0], selected[1], PieceType.EMPTY)

    print(f'available squares: {available_squares(x, y)}')

# function to check if a move is valid
def check_move(x, y, x2, y2):
    # check if move is diagonal
    if abs(x - x2) != abs(y - y2):
        return False

    # check if move is 1 square
    if abs(x - x2) != 1:
        return False

    # check if move is in bounds
    if x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7:
        return False

    # check if move is empty
    if board[y2][x2] != 0:
        return False

    # check if move is in correct direction
    if board[y][x] == 1 and y2 > y:
        return False

    if board[y][x] == 2 and y2 < y:
        return False

    # check if move is a jump
    if abs(x - x2) % 2 == 0:  # accounts for all jump magnitudes
        if board[(y + y2) // 2][(x + x2) // 2] == 0: # check if piece exists
            return False
        else:
            board[(y + y2) // 2][(x + x2) // 2] = 0 # remove piece
            return True
    return True

# create the animation for the checker piece to move
def move_piece(x, y, x2, y2):
    # check if the move is valid
    if check_move(x, y, x2, y2):
        # move the piece
        board[y2][x2] = board[y][x]
        # set previous piece to empty
        board[y][x] = Piece(x, y, PieceType.EMPTY, False, False, False)
        # check if the piece is a king
        if board[y2][x2].type == PieceType.WHITE and y2 == 7:
            board[y2][x2].king = True
        if board[y2][x2] == PieceType.BLACK and y2 == 0:
            board[y2][x2].king = True
        # check if the move is a jump
        match abs(x - x2):
            case 2:
                board[(y + y2) // 2][(x + x2) // 2].type = PieceType.EMPTY
                return 'jump'
            # check if the move is a double jump
            case 4:
                board[(y + y2) // 2][(x + x2) // 2].type = PieceType.EMPTY
                board[(y + y2) // 2][(x + x2) // 2].type = PieceType.EMPTY
                return 'double jump'
            # check if the move is a triple jump
            case 6:
                board[(y + y2) // 2][(x + x2) // 2].type = PieceType.EMPTY
                board[(y + y2) // 2][(x + x2) // 2].type = PieceType.EMPTY
                board[(y + y2) // 2][(x + x2) // 2].type = PieceType.EMPTY
                return 'triple jump'

# highlight moves
def highlight_moves(xy, rm):
    h = Turtle()
    h.hideturtle()
    h.penup()
    for i in xy:
        x = i[0]
        y = i[1]
        h.goto(x * 60 - 260, y * -60 + 200)
        h.stamp()
        h.forward(15)
        h.right(90)
        h.forward(30)
        if rm == True:
            h.color("#8b4513")
        else:
            h.color("#003e92")
        h.begin_fill()
        h.circle(15)
        print(h.pos())
        h.end_fill()
        h.color(0, 0, 0)
        h.back(30)
        h.left(90)
        h.back(30)

window.onscreenclick(mouse_event)

t.goto(-200, 200)
t.stamp()
input("Press enter to exit...")
mainloop()


# 0 [[0, 1, 0, 3, 0, 5, 0, 7],
# 1 [0, 0, 2, 0, 4, 0, 6, 0],
# 2 [0, 0, 0, 0, 0, 0, 0, 0],
# 3 [0, 0, 0, 0, 0, 0, 0, 0],
# 4 [0, 0, 0, 0, 0, 0, 0, 0],
# 5 [0, 0, 0, 0, 0, 0, 0, 0],
# 6 [0, 0, 0, 0, 0, 0, 0, 0],
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
