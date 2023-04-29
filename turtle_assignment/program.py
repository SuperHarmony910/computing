from enum import Enum
from turtle import *

# setting
setup(0.5401041667, 0.80546875, 0.5, 0.5)
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
speed(0)  # 0 = fastest, 1 = slowest - adjust before submission!
tracer(0, 0)  # instant drawing (no animation), very useful for debugging

# position to top left corner
penup()
left(90)
forward(200)
left(90)
forward(200)
left(180)
pendown()


# create an enum for the pieces
class PieceType(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    WHITE_KING = 3
    BLACK_KING = 4
    WHITE_SELECTED = 5
    BLACK_SELECTED = 6
    WHITE_KING_SELECTED = 7
    BLACK_KING_SELECTED = 8
    WHITE_MOVE = 9
    BLACK_MOVE = 10
    WHITE_KING_MOVE = 11
    BLACK_KING_MOVE = 12

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


checker_pieces = {}  # y, x, type
# ^^ think about renaming var to 'board' when time permits after commit (its late and im tired)
# function to create a checker piece from top right corner of square


def create_piece(type):
    if type == "white":
        color("#d2b26d", "#e9ce9b")
    else:
        color("#1b100b", "#300c09")
    pensize(3)
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
    # print(i)

# create final square
create_square(1)

# back to original pos
penup()
right(90)
forward(120)
right(90)
forward(120)
right(90)

# use board array to put pieces in correct positions
for y in range(8):
    for x in range(8):
        if (y + x) % 2 != 0:
            forward(60*x)
            right(90)
            forward(60*y)
            left(90)
            if y < 3:
                checker_pieces[int(round(pos()[1]-200)/-60)][int(round(pos()[0]+260)/60)] = pos()[1]/60, pos()[0]/60, "white"
                create_piece("white")
            elif y > 4:
                checker_pieces[int(round(pos()[1]-200)/-60)][int(round(pos()[0]+260)/60)] = pos()[1]/60, pos()[0]/60, "black"
                create_piece("black")

            # return to original pos
            back(60*x)
            right(90)
            back(60*y)
            left(90)

# draw the coordinate of each square on the board
# this is for debugging purposes
for y in range(8):
    for x in range(8):
        forward(60*x)
        right(90)
        forward(60*y+30)
        left(90)
        forward(30)
        color('deepskyblue')
        write(str(x) + ", " + str(y), align="center",
              font=("Arial", 18, "normal"))
        color('black')
        back(30)
        back(60*x)
        right(90)
        back(60*y+30)
        left(90)

# log checker pieces dict
print(checker_pieces)

# make this checkers board playable
# 0 = empty, 1 = white, 2 = black
# 3 = white king, 4 = black king
# 5 = white selected, 6 = black selected
# 7 = white king selected, 8 = black king selected
# 9 = white move, 10 = black move
# 11 = white king move, 12 = black king move

# create a class for the pieces


class Piece:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.king = False
        self.selected = False

# select a piece to move


def select_piece(x, y):
    match board[y][x]:
        # check if the selected piece is a white piece
        case PieceType.WHITE:
            if board[y][x] == PieceType.WHITE_SELECTED:
                return PieceType.EMPTY
            else:
                return PieceType.WHITE_SELECTED
        # check if the selected piece is a black piece
        case PieceType.BLACK:
            if board[y][x] == PieceType.BLACK_SELECTED:
                return PieceType.EMPTY
            else:
                return PieceType.BLACK_SELECTED
        # check if the selected piece is a white king
        case PieceType.WHITE_KING:
            if board[y][x] == PieceType.WHITE_KING_SELECTED:
                return PieceType.EMPTY
            else:
                return PieceType.WHITE_KING_SELECTED
        # check if the selected piece is a black king
        case PieceType.BLACK_KING:
            if board[y][x] == PieceType.BLACK_KING_SELECTED:
                return PieceType.EMPTY
            else:
                return PieceType.BLACK_KING_SELECTED
        # check if the selected piece is nonexistent
        case _:
            return PieceType.EMPTY


# create the animation for the checker piece to move
def move_piece(x, y, x2, y2):
    # check if the move is valid
    if check_move(x, y, x2, y2):
        # move the piece
        board[y2][x2] = board[y][x]
        board[y][x] = PieceType.EMPTY
        # check if the piece is a king
        if board[y2][x2] == PieceType.WHITE and y2 == 7:
            board[y2][x2] = PieceType.WHITE_KING
        if board[y2][x2] == PieceType.BLACK and y2 == 0:
            board[y2][x2] = PieceType.BLACK_KING
        # check if the move is a jump
        match abs(x - x2):
            case 2:
                board[(y + y2) // 2][(x + x2) // 2] = PieceType.EMPTY
                return 'jump'
            # check if the move is a double jump
            case 4:
                board[(y + y2) // 2][(x + x2) // 2] = PieceType.EMPTY
                board[(y + y2) // 2][(x + x2) // 2] = PieceType.EMPTY
                return 'double jump'
            # check if the move is a triple jump
            case 6:
                board[(y + y2) // 2][(x + x2) // 2] = PieceType.EMPTY
                board[(y + y2) // 2][(x + x2) // 2] = PieceType.EMPTY
                board[(y + y2) // 2][(x + x2) // 2] = PieceType.EMPTY
                return 'triple jump'


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
        if board[y][x] == 1:
            if board[y2 + 1][x2 + 1] != 2 and board[y2 + 1][x2 - 1] != 2:
                return False
        if board[y][x] == 2:
            if board[y2 - 1][x2 + 1] != 1 and board[y2 - 1][x2 - 1] != 1:
                return False
    return True


# function to check if a jump is valid
def check_jump(x, y, x2, y2):
    # check if jump is diagonal
    if abs(x - x2) != abs(y - y2):
        return False
    # check if jump is 2 squares
    if abs(x - x2) != 2:
        return False
    # check if jump is in bounds
    if x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7:
        return False
    # check if jump is empty
    if board[y2][x2] != 0:
        return False
    # check if jump is in correct direction
    if board[y][x] == 1 and y2 > y:
        return False
    if board[y][x] == 2 and y2 < y:
        return False
    # check if jump is over an enemy piece
    if board[y][x] == 1:
        if x2 > x and board[y + 1][x + 1] != 2:
            return False
        if x2 < x and board[y + 1][x - 1] != 2:
            return False
    if board[y][x] == 2:
        if x2 > x and board[y - 1][x + 1] != 1:
            return False
        if x2 < x and board[y - 1][x - 1] != 1:
            return False
    return True

# function to check if a piece can jump


def check_jump_available(x, y):
    match board[y][x]:
        case 1:
            if x > 1 and check_jump(x, y, x - 2, y + 2):
                return True
            if x < 6 and check_jump(x, y, x + 2, y + 2):
                return True
        case 2:
            if x > 1 and check_jump(x, y, x - 2, y - 2):
                return True
            if x < 6 and check_jump(x, y, x + 2, y - 2):
                return True
        case _:
            return False

# make piece jump


def jump(x, y, x2, y2):
    board[y2][x2] = board[y][x]
    board[y][x] = 0
    # check if piece becomes king
    if board[y2][x2] == PieceType.WHITE and y2 == PieceType.WHITE_KING_SELECTED:
        board[y2][x2] = PieceType.WHITE_KING
    if board[y2][x2] == PieceType.BLACK and y2 == 0:
        board[y2][x2] = PieceType.BLACK_KING
    if abs(x - x2) == 2:
        # remove enemy piece
        if board[y2][x2] == 1:
            if x2 > x:
                board[y2 - 1][x2 - 1] = PieceType.EMPTY
            if x2 < x:
                board[y2 - 1][x2 + 1] = PieceType.EMPTY
        if board[y2][x2] == 2:
            if x2 > x:
                board[y2 + 1][x2 - 1] = PieceType.EMPTY
            if x2 < x:
                board[y2 + 1][x2 + 1] = PieceType.EMPTY

goto(-200, 200)
stamp()
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
