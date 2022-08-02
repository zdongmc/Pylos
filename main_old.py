

# #play jump method
# # def play_jump(board, level,row, column, color, rC, bC):
# #   if

# #not class methods
# #changes the first character of the string
    


# #change a tile
# def play(board, level, row, column, color, rC, bC):# when adding 
#   if(board[level][row][column] == "EA"):
#     if((color == 'B' or color == "B") and (bC > 0)):
#       board[level][row][column] = color+"U"
#       refresh_availability(board)
#       bC = bC - 1
#     elif((color == "R" or color == 'R') and (rC > 0)):
#       board[level][row][column] = color+"U"
#       refresh_availability(board)
#       rC = rC -1
#     else:
#       print("Out of counters")
#   else:
#     print("You cannot play in that space")

# #output the current board
# def outputBoard(board):
#   for level in board:
#     print()
#     for row in level: #fi is a list
#       print(row)

# #initialize the board
# def initialize(b):
#   for i in range(4):
#       b.append([])
#       for j in range(b.__len__()):
#           b[i].append([])
#           for k in range(b.__len__()):
#               b[i][j].append("EU")
  
#   #making the lowest level available
#   for i in range(b.__len__()):
#     for j in range(b.__len__()):
#       b[b.__len__()-1][i][j] = "EA"
#   outputBoard(board)

# #this method changes the availability of spaces if there is square to step on 
# def refresh_availability(b):
#   for i in range(b.__len__() - 1):
#     for j in range(b[i].__len__()):
#       for k in range(b[i][j].__len__()):
#         if (b[i][j][k] == 'EU' and \
#         (b[i+1][j][k] == 'BU'or b[i+1][j][k] == 'RU' )and \
#         (b[i+1][j+1][k] == 'BU' or b[i+1][j+1][k] == 'RU')and \
#         (b[i+1][j][k+1] == 'BU'or b[i+1][j][k+1] == 'RU')and \
#         (b[i+1][j+1][k+1]== 'BU'or b[i+1][j+1][k+1]== 'RU')):
#           b[i][j][k] = 'EA'


# #take the board and color that you want to check
# #whenever a new piece is played check and change the pieces below it from BA to Bu and same for red
          
# #main
# board = []
# redCounters = 15
# blueCounters = 15

# initialize(board)
# outputBoard(board)

# valid = 'y'

# color = 'E'
# while(valid == 'y'):
#   level = int(input())
#   row = int(input())
#   col = int(input())
#   color = input()
#   play(board, level,row,col,color, redCounters, blueCounters)
#   outputBoard(board)
#   valid = input()


## this is the updated code







# class, ignore for now
class space:
    def __init__(self):
        self.color = "e"
        self.available = True

    def play(self, color):
        self.color = color
        self.available = False

    def output(self):
        print("Color: " + self.color)
        print("Availiability: " + self.availiable)


# return available spaces
def show_available_spaces(b):
  moves = 0  
  for i in range(b.__len__()):
        for j in range(b[i].__len__()):
            for k in range (b[i][j].__len__()):
              if b[i][j][k] == "EA":
                  print("level: ", i,  " col: " , j , "row: " ,k)
                  moves = moves + 1
  print('number of moves = ', moves)


# play jump method
# def play_jump(board, level,row, column, color, rC, bC):
#   if

# not class methods
# changes the first character of the string


def play(b, level, row, column, color, bC, rC):  # when adding new pebble to the board
    if b[level][column][row] == 'EA':
        if (color == 'B' and bC > 0):
            b[level][column][row] = color + "U"
            refresh_availability(b)
            bC = bC - 1
        elif (color == 'R' and rC) > 0:
            b[level][column][row]= color + "U"
            refresh_availability(b)
            rC = rC - 1
        else:
            print("Out of counters")
    else:
        print("You cannot play in that space")


def output_board(b):
    for each in b:

        for fi in each:  # fi is a list
            print(fi)
        print()


# returns perfectly initialized board
def create_and_fill(levels):
    b = []
    for i in range(levels):
        b.append([])
        for j in range(b.__len__()):
            b[i].append([])
            for k in range(b.__len__()):
                b[i][j].append("EU")

        # making the lowest level available
    for i in range(b.__len__()):
        for j in range(b.__len__()):
            b[b.__len__() - 1][i][j] = "EA"
    return b


# main
board = create_and_fill(4)
redCounters = 15
blueCounters = 15
# output_board(board)


# this method changes the availability of spaces if there is square to step on
def refresh_availability(b):
    for i in range(b.__len__() - 1):
        for j in range(b[i].__len__()):
            for k in range(b[i][j].__len__()):
                if (b[i + 1][j][k] == 'BU' or b[i + 1][j][k] == 'RU') and \
                        (b[i + 1][j + 1][k] == 'BU' or b[i + 1][j + 1][k] == 'RU') and \
                        (b[i + 1][j][k + 1] == 'BU' or b[i + 1][j][k + 1] == 'RU') and \
                        (b[i + 1][j + 1][k + 1] == 'BU' or b[i + 1][j + 1][k + 1] == 'RU'):
                    b[i][j][k] = 'EA'


#
# print(board[i].__len__())

play(board, 3, 0, 0, "B", redCounters, blueCounters)
play(board, 3, 1, 0, "R", redCounters, blueCounters)
play(board, 3, 0, 1, "B", redCounters, blueCounters)
play(board, 3, 1, 1, "R", redCounters, blueCounters)

# board[3][1][1] = 'RU'
# board[3][2][1] = 'RU'
# board[3][1][2] = 'BU'
# board[3][2][2] = 'RU'


# output_board(board)

# I want to see if there is a better way of doing this
# play(board, 3, 0, 0, "B", redCounters, blueCounters)
# output_board(board)


# Notes
# First parameter is which level to play on
# Second parameter is the row
# Third is the column


# # I am going to try to analyze the game with three levels( like build a game tree for it)
# small_red_counters = 7
# small_blue_counters = 7

#small_board = create_and_fill(3)
#output_board(small_board)
#show_available_spaces(small_board)
# # top left square on the third level
# play(small_board, 2, 0, 0, "B", small_red_counters, small_blue_counters)
# play(small_board, 2, 1, 0, "R", small_red_counters, small_blue_counters)
# play(small_board, 2, 0, 1, "B", small_red_counters, small_blue_counters)
# play(small_board, 2, 1, 1, "R", small_red_counters, small_blue_counters)

# # make others  available
# play(small_board, 2, 2, 0, "B", small_red_counters, small_blue_counters)
# play(small_board, 2, 2, 1, "R", small_red_counters, small_blue_counters)
# play(small_board, 2, 2, 2, "B", small_red_counters, small_blue_counters)
# play(small_board, 2, 0, 2, "R", small_red_counters, small_blue_counters)
# play(small_board, 2, 1, 2, "B", small_red_counters, small_blue_counters)

# # make all

# method to jump
#
# def jump (b, from_level, from_column, from_row, to_level, to_column, to_row):
#     # if the To position is available after the From postion is empty then jumping is available
#     x = b[from_level][from_column][from_row]
#     b[from_level][from_column][from_row]  = "EA"
#     if b[]
#

# output_board(small_board)
# def make_last_move(b,level, column, row, red, blue):
#     for i in range(b.__len__() - 1):


def position(b, level, column, row, color, red, blue,starter):
    if (starter == red and blue == 0) or (starter == blue and red ==0):
        return "N"
    if (starter == red and red == 0) or (starter == blue and blue == 0):
        return "P"
    if red == 0:
        return "L"
    if blue == 0:
        return "R"
    return 34

def get_next_color(color, bC, rC):
  next_color = color # default
  if(rC <=0 and bC <=0):
    print("Warning: OUT OF MARBLES")
  if ((color == "R") and (bC > 0)):
      next_color = "B"
  else:
    if ((color == "B") and (rC > 0)):
      next_color = "R"
  return next_color
  
  
#Make Game Tree
def make_tree(b, color, bC, rC): 
  for i in range(b.__len__()):
        for j in range(b[i].__len__()):
            for k in range (b[i][j].__len__()):
              if b[i][j][k] == "EA":
                  print("Playing ", color, " on level: ", i,  " col: " , j , "row: " ,k)
                  play(b, i, j, k, color, bC, rC)
                  output_board(b)
                  color = get_next_color(color, bC, rC)
                  make_tree(b, color, bC, rC)
            print(b[0][0][0], "wins")


# show_available_spaces(small_board)

#Analyze 2x2 board
twoxtwo_board = create_and_fill(2)
print('initalized board')
output_board(twoxtwo_board)

color = "B"

bC = 3
rC = 3
play(twoxtwo_board, 1, 0, 0, color, bC, rC)
print("counters:", bC, rC)
color = get_next_color(color, bC, rC)
play(twoxtwo_board, 1, 1, 1, color, bC, rC)
output_board(twoxtwo_board)
print("counters:", bC, rC)
#color = get_next_color(color, bC, rC)

#make_tree(twoxtwo_board, color, bC, rC)

