from enum import IntEnum
import math
from turtle import Turtle, Screen, setup, tracer, mainloop

t = Turtle()
writer = Turtle()
writer.penup()
writer.hideturtle()

# setting
setup(0.5401041667, 0.80546875, 0.5, 0.5)
window = Screen()
window.title("Checkers Assignment")
window.bgcolor("darkslateblue")

# quick speed for faster debugging
t.speed(0)  # 0 = fastest, 1 = slowest - adjust before submission!
tracer(0, 0)  # instant drawing (no animation), very useful for debugging

i = 7  # square iterator
c = 0  # colour iterator
board = []  # board array
selected = [0, 0, False]  # if a piece is selected or not

t.penup()
t.goto(-200, 350)
font = ("monospace", 30, "normal")
t.write('Checkers Assignment', font=font)
t.goto(0, 0)
t.pd()

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
    WHITE_MOVE = 3  # 9
    BLACK_MOVE = 4  # 10
    # WHITE_KING_MOVE = 11
    # BLACK_KING_MOVE = 12


move = PieceType.BLACK


class Piece:
    def __init__(self, x, y, type: PieceType, king=False, selected=False):
        self.x = x
        self.y = y
        self.type: PieceType = type
        self.king = king
        self.selected = selected


for i in range(8):
    board.append([])
    for j in range(8):
        board[i].append(Piece(i, j, PieceType.EMPTY))


# position to top left corner
t.penup()
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(180)
t.pendown()


# function to create a square
def create_square(endfill=0, replace=False):
    global c
    t.pendown()
    if endfill == 1:
        c = 1
        t.forward(60)
        t.right(90)
        t.forward(60)
    if replace == True:
        c = 0
        t.pensize(0)
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
    t.penup()


def create_piece(type: PieceType):
    checker = t
    if type == PieceType.WHITE:
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
                create_piece(PieceType.WHITE)
            elif y > 4:
                board[int(round(t.pos()[1]-200)//-60)
                      ][int(round(t.pos()[0]+260)//60)].type = PieceType.BLACK
                create_piece(PieceType.BLACK)

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

# create the animation for the checker piece to move


def move_piece(x, y, x2, y2):
    if [x2, y2] not in available_squares(x, y):
        return False
    # check if the move is valid
    if check_move(x, y, x2, y2):
        # move the piece
        print(f'took off: {x}, {y} - landed: {x2}, {y2}')
        board[y2][x2] = board[y][x]
        animate_move(x, y, x2, y2)
        print(f'black piece moved to: {x2}, {y2}')
        # set previous piece to empty
        board[y][x] = Piece(x, y, PieceType.EMPTY)
        # check if the piece is a king
        if board[y2][x2].type == PieceType.WHITE and y2 == 7:
            board[y2][x2].king = True
            king_piece(x2, y2)
        if board[y2][x2] == PieceType.BLACK and y2 == 0:
            print('black king')
            board[y2][x2].king = True
            king_piece(x2, y2)
        print('kinged?', board[y2][x2].king)
        # check if move is jump. if move is not jump, default case will handle move


# check which squares are available


def available_squares(x, y):
    def try_except(x, y, tested_type=PieceType.EMPTY):
        if x < 0 or y < 0:
            return False
        if tested_type == PieceType.EMPTY:  # this is for regular jumps
            try:
                if board[y][x].type == tested_type:
                    return True
            except IndexError:
                pass
            return False
        else:  # this is for taking pieces
            try:
                if board[y][x].type == tested_type:
                    return True
            except IndexError:
                pass
            return False
    available_squares = []
    # make sure coordinate is not out of bounds
    if x < 8 and y < 8:
        if x > -1 and y > -1:
            if board[y][x].type == PieceType.BLACK:
                if try_except(x+1, y-1):  # possibility one
                    available_squares.append([x+1, y-1])
                if try_except(x-1, y-1):  # possibility two
                    available_squares.append([x-1, y-1])

                if board[y][x].king == True:  # if a king
                    if try_except(x+1, y-1):  # possibility three as king
                        available_squares.append([x+1, y-1])
                    if try_except(x-1, y+1):  # possibility four as king
                        available_squares.append([x-1, y+1])

                try:
                    if board[y+1][x+1].type == PieceType.WHITE and board[y+2][x+2].type == PieceType.EMPTY:
                        available_squares = [[x+2, y+2]]
                except IndexError:
                    print('index error')
                    pass

                try:
                    if board[y-1][x+1].type == PieceType.WHITE and board[y-2][x+2].type == PieceType.EMPTY:
                        available_squares = [[x+2, y-2]]
                except IndexError:
                    pass

                try:
                    if board[y+1][x-1].type == PieceType.WHITE and board[y+2][x-2].type == PieceType.EMPTY:
                        available_squares = [[x-2, y+2]]
                except IndexError:
                    pass

                try:
                    if board[y-1][x-1].type == PieceType.WHITE and board[y-2][x-2].type == PieceType.EMPTY:
                        available_squares = [[x-2, y-2]]
                except IndexError:
                    pass

            if board[y][x].type == PieceType.WHITE:
                if try_except(x+1, y+1):
                    available_squares.append([x+1, y+1])
                if try_except(x-1, y+1):
                    available_squares.append([x-1, y+1])
                if board[y][x].king == True:
                    if try_except(x+1, y-1):
                        available_squares.append([x+1, y-1])
                    if try_except(x-1, y-1):
                        available_squares.append([x-1, y-1])
                if y > 6:  # you cant take a piece on the seventh rank
                    return available_squares
                try:
                    if board[y+1][x+1].type == PieceType.BLACK and try_except(x+2, y+2):
                        available_squares = [[x+2, y+2]]
                except IndexError:
                    pass
                try:
                    if board[y-1][x+1].type == PieceType.BLACK and try_except(x+2, y-2):
                        available_squares = [[x+2, y-2]]
                except IndexError:
                    pass
                try:
                    if board[y+1][x-1].type == PieceType.BLACK and try_except(x-2, y+2):
                        available_squares = [[x-2, y+2]]
                except IndexError:
                    pass
                try:
                    if board[y-1][x-1].type == PieceType.BLACK and try_except(x-2, y-2):
                        available_squares = [[x-2, y-2]]
                except IndexError:
                    pass

    return available_squares


# get clicked coordinates
def mouse_event(xraw, yraw):  # returns x, y, is_move_to
    global selected
    global move
    y = math.floor(round(yraw-200)//-60)
    x = math.floor(round(xraw+260)//60)
    if y > 7 or x > 7 or x < 0 or y < 0:
        return False  # print('out of bounds')

    # check if piece was actually moved before changing move variable to signify which player's turn it is

    if selected[2] == True:
        highlight_moves(available_squares(x, y), True)
        move_piece(selected[0], selected[1], x, y)
        selected[0] = False
        selected[1] = False
        selected[2] = False
        # return x, y, True
    else:
        highlight_moves(available_squares(x, y), False)
        selected[0] = x
        selected[1] = y
        selected[2] = True
    # return x, y, False

    try:
        board[selected[0]][selected[1]].selected = selected[2]
        print(f'coords: {x}, {y}, available squares: {available_squares(x, y)}, type: {board[y][x].type}')
    except:
        board[selected[0]][selected[1]] = Piece(
            selected[0], selected[1], PieceType.EMPTY)

    # write who's turn it is
    if selected[2] == False:
        if board[y][x].type == PieceType.BLACK:
            move = PieceType.WHITE
            writer.clear()
            writer.goto(-100, 220)
            writer.write('its whites turn', font=font)
        elif board[y][x].type == PieceType.WHITE:
            move = PieceType.BLACK
            writer.clear()
            writer.goto(-100, 220)
            writer.write('its blacks turn', font="Arial, 30")

# function to check if a move is valid


def check_move(x, y, x2, y2):
    # check if move is diagonal
    if abs(x - x2) != abs(y - y2):
        return False

    # invalidate king moves to non king pieces
    if board[y][x].king == False and y2 > y:
        if board[y][x].type == PieceType.BLACK:
            return False
    if board[y][x].king == False and y2 < y:
        if board[y][x].type == PieceType.WHITE:
            return False

    # check if move is in bounds
    if x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7:
        return False

    # check if move is empty
    if board[y2][x2].type != PieceType.EMPTY:
        return False
    return True

# create the animation for the checker piece to move


def animate_move(x, y, x2, y2):
    t.goto(x * 60 - 260, y * -60 + 200)
    create_square(False, True)
    t.goto(x2 * 60 - 260, y2 * -60 + 200)
    create_piece(board[y][x].type)
    # check if move is a jump
    if abs(x - x2) % 2 == 0:  # accounts for all jump magnitudes
        if board[(y + y2) // 2][(x + x2) // 2]:  # look for the piece in the middle

            t.goto(((x + x2) // 2) * 60 - 260, ((y + y2) // 2) * -60 + 200)
            create_square(False, True)


def king_piece(x, y):
    print('KINGED')
    t.goto(x * 60 - 260, y * -60 + 200)
    t.right(90)
    t.fd(30)
    # set colour to gold
    t.color("#ffd700", "#ffd700")
    t.circle(15)


# highlight moves
unhighlight = []


def highlight_moves(xy, rm: bool):
    global unhighlight
    h = Turtle()
    h.hideturtle()
    h.penup()
    # remove previous highlight
    for x, y in unhighlight:
        if board[y][x].type != PieceType.EMPTY:
            continue
        h.goto(x * 60 - 260, y * -60 + 200)
        h.forward(15)
        h.right(90)
        h.forward(30)
        h.color("#8b4513")
        h.begin_fill()
        h.circle(15)
        h.end_fill()
        h.color(0, 0, 0)
        h.back(30)
        h.left(90)
        h.back(30)

    # create highlight
    for i in xy:
        x = i[0]
        y = i[1]
        h.goto(x * 60 - 260, y * -60 + 200)
        h.forward(15)
        h.right(90)
        h.forward(30)
        if rm == True:
            h.color("#8b4513")
        else:
            h.color("#003e92")
        h.begin_fill()
        h.circle(15)
        h.end_fill()
        h.color(0, 0, 0)
        h.back(30)
        h.left(90)
        h.back(30)
        unhighlight.append([x, y])


window.onscreenclick(mouse_event)

t.goto(-200, 200)
t.stamp()
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
