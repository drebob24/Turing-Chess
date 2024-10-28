## Dictionary to keep track of what black pieces can be placed
available_pieces = {
        "pawn" : 8,
        "rook" : 2,
        "knight" : 2,
        "bishop" : 2,
        "king" : 1,
        "queen" : 1
    }

def main():

#Create Chess Board
    current_board = create_board()
    print_board(current_board)
#Ask user to place a white piece
    white = ask_for_white(current_board)
#Print board
    current_board = update_board(white, current_board, "white")
    print_board(current_board)

#Ask user to place black pieces, at least 1, up to 16
    current_board = get_black_pieces(current_board)
    
#Determine what pieces White can take
    print(analyze_board(current_board, white))

def create_board():
    chess_board = {
        "a1": "-", "b1": "-", "c1": "-", "d1": "-", "e1": "-", "f1": "-", "g1": "-", "h1": "-",
        "a2": "-", "b2": "-", "c2": "-", "d2": "-", "e2": "-", "f2": "-", "g2": "-", "h2": "-",
        "a3": "-", "b3": "-", "c3": "-", "d3": "-", "e3": "-", "f3": "-", "g3": "-", "h3": "-",
        "a4": "-", "b4": "-", "c4": "-", "d4": "-", "e4": "-", "f4": "-", "g4": "-", "h4": "-",
        "a5": "-", "b5": "-", "c5": "-", "d5": "-", "e5": "-", "f5": "-", "g5": "-", "h5": "-",
        "a6": "-", "b6": "-", "c6": "-", "d6": "-", "e6": "-", "f6": "-", "g6": "-", "h6": "-",
        "a7": "-", "b7": "-", "c7": "-", "d7": "-", "e7": "-", "f7": "-", "g7": "-", "h7": "-",
        "a8": "-", "b8": "-", "c8": "-", "d8": "-", "e8": "-", "f8": "-", "g8": "-", "h8": "-"
    }

    return chess_board

def print_board(board):
    #create a list for the row
    row = ["1"]
    print("")
    print("    A   B   C   D   E   F   G   H  ")
    print("   --- --- --- --- --- --- --- --- ")
    for space in board:
       #add contenct of each space to the row list
       row.append(board[space])
       #Need to cut off row at H and start the next one
       if space[0] == "h":
           #output list contents split by | dividers
           print(" | ".join(row) + " |")
           print("   --- --- --- --- --- --- --- --- ")
           ##Grab next row's label using current row value
           new_row = int(space[1]) + 1
           row = [str(new_row)]
    print("    A   B   C   D   E   F   G   H  ")

def ask_for_white(game_board):
    print("")
    print("Please place a White piece on the board, either a Rook or a Pawn.")
    print("In the case of a pawn, the piece will be as if White started from the Top (Row 1)")
    print("Enter in the format: rook a4")
    #Loop until valid input
    while True:
        user_input = input("Your selection: ").lower().strip()
        #Seperate validity check into seperate function so it can easily be used for black pieces
        if check_valid(user_input, "white", game_board):
            break
        else:
            continue
    return user_input

def update_board(user_choice, board_update, color):
    spot = user_choice.split()[1]
    piece = user_choice.split()[0]
    #piece stored as first initial unless knight due ot knight:king conflict
    if color == "white":
        board_update[spot] = piece[0].upper()
    elif color == "black":
        if piece == "knight":
            board_update[spot] = "h"
        else:    
            board_update[spot] = piece[0].lower()
    return board_update

def check_valid(input_text, color, gameboard):
    global available_pieces
    #Make sure input isn't pushed together 'rooka4'
    if " " not in input_text:
        print('ERROR: Invalid input, please format as "rook a4" with a space.')
        return False
    #Correct format will put the space in the second spot of a split list
    if input_text.split()[1] not in gameboard:
        print("ERROR: Invalid space.")
        return False
    #Need to seperate white and black due to possible inputs
    elif color == "white":
        if "pawn" not in input_text and "rook" not in input_text:
            print("ERROR: Invalid piece.")
            return False
        else:
            return True
    elif color == "black":
        chosen_piece = input_text.split()[0]
        if chosen_piece not in available_pieces:
            print("ERROR: Invalid piece")
            return False
        elif available_pieces[chosen_piece] == 0:
            print("ERROR: No " + chosen_piece.capitalize() + "s remaining. Choose a different piece.")
            return False
        elif gameboard[input_text.split()[1]] != "-":
            print("ERROR: Space already taken.")
            return False
        else:
            return True

def get_black_pieces(game_board):
    global available_pieces
    print("")
    print("Please select where to place a black piece.")
    print("You must place at least one, and can place up to 16 pieces.")
    print("Any kind of piece can be placed:")
    print("8 Pawns (p), 2 Rooks (r), 2 Knights (h), 2 Bishops (b), 1 King (k), 1 Queen(q)")
    print('When you are done, simply type "done"')
    print("The format is the same: rook a4")
    ##Loop until all pieces used or user terminates loop
    while sum(available_pieces.values()) > 0:
        black = input("Your selection: ").lower().strip()
        if sum(available_pieces.values()) == 16 and black == "done":
            print("ERROR: You must place at least on piece")
            continue
        elif black == "done":
            break
        else:
            if check_valid(black, "black", game_board):         
                new_board = update_board(black, game_board, "black")
                print_board(new_board)
                ##Had updating the piece list included here but code felt messy so seperated it to a new function
                update_black_pieces(black)
            else:
                continue
    return new_board

def update_black_pieces(chosen_piece):
    global available_pieces
    available_pieces[chosen_piece.split()[0]] -= 1
    if sum(available_pieces.values()) > 0:
        print(str(sum(available_pieces.values())) + " pieces left:", end="")
        for bp in available_pieces:
            print(" " + bp.capitalize() + "s: " + str(available_pieces[bp]), end="")
        print("")
    else:
        print("All pieces placed.")

def analyze_board(final_board, white_input):
    input("I will now calculate what pieces White can take: <Press Enter>")
    white_type = white_input.split()[0]
    white_loc = white_input.split()[1]
    if white_type == "pawn":
        target_list = pawn_logic(white_loc, final_board)
        if target_list == []:
            return "White Pawn cannot take any pieces."
        else:
            return "White Pawn can take:" + identify_pieces(target_list, final_board)
    else:
        target_list = rook_logic(white_loc, final_board)
        if target_list == []:
            return "White Rook cannot take any pieces."
        else:
            return "White Rook can take:" + identify_pieces(target_list, final_board)

def pawn_logic(loc, chessboard):
    #Take location. To find out where pawn can attack:
    # 2 spots: 1 down and 1 to the left of loc, 1 down and 1 to the right of loc
    #If pawn at last row it cannot attack anything.
    if loc[1] == "8":
        return "[]"
    col = loc[0]
    row = int(loc[1])
    #col is a character so need to convert it to a number, subtract 96 to normalize it to a = 1
    num_col = ord(col) - 96
    if 0 < num_col < 7:
        target_one = chr(num_col - 1 + 96) + str(row + 1)
        target_two = chr(num_col + 1 + 96) + str(row + 1)
        #Check if there are pieces at those spots, if not, remove them
        can_be_taken = check_spaces([target_one, target_two], chessboard)
    #if at column A, can only attack to the right
    elif num_col == 0:
        target = chr(num_col + 1 + 96) + str(row + 1)
        can_be_taken = check_spaces([target], chessboard)
    #only leaves the column H case
    else:
        target = chr(num_col - 1 + 96) + str(row + 1)
        can_be_taken = check_spaces([target], chessboard)

    return can_be_taken

def check_spaces(targets, chessboard):
    i = 0
    while i in range(len(targets)):
        #remove space from list if empty
        if chessboard[targets[i]] == "-":
            targets.pop(i)
        else:
            i += 1
    return targets


def identify_pieces(locations, chessboard):
    taken = ""
    for space in locations:
        match chessboard[space]:
            case 'p': 
                taken = taken + " Black Pawn " + space.upper()
            case 'h':
                taken = taken + " Black Knight " + space.upper()
            case 'r':
                taken = taken + " Black Rook " + space.upper()
            case 'b':
                taken = taken + " Black Bishop " + space.upper()
            case 'k':
                taken = taken + " Black King " + space.upper()
            case 'q':
                taken = taken + " Black Queen " + space.upper()
    return taken

def rook_logic(loc, chessboard):
    #Rook can at most take 4 different pieces, one in each direction
    #ID column and row, create 4 lists, up, down, left, right, find first piece in each list
    up = []
    down = []
    left = []
    right = []
    #Count spaces upwards, starting from the space above white
    for i in range(int(loc[1])-1, 0, -1):
        up.append(loc[0] + str(i))
    #Count spaces downards, starting from space below white
    for i in range(int(loc[1])+1, 9):
        down.append(loc[0] + str(i))
    #Convert column into numberic value (a = 0), to then create left and right lists
    num_col = ord(loc[0]) - 96
    for i in range(num_col - 1, 0, -1):
        left.append(chr(i + 96) + loc[1])
    for i in range(num_col + 1, 9):
        right.append(chr(i + 96) + loc[1])
    #Remove empty spaces from lists, crate final target list which will be the first value remaining in the lists
    final_list = []
    #Need empty checks to avoid call errors.
    if up:
        up = check_spaces(up, chessboard)
        if up: final_list.append(up[0])
    if down:
        down = check_spaces(down, chessboard)
        if down: final_list.append(down[0])
    if left:
        left = check_spaces(left, chessboard)
        if left: final_list.append(left[0])
    if right:
        right = check_spaces(right, chessboard)
        if right: final_list.append(right[0])
    
    return final_list


main()

##Assumptions:##
#White will start from Top, important for direction pawns can attack
#White represented as Capital letters, black represented as lower case
#The 16 black pieces that can be placed can be any pieces (knight=h for horse, rook, pawn, bishop, king, queen) of any amount
#   since black does not act in this program, piece type does not really matter
#   if have more time, will add code to limit 8 pawns, 2 bishops, knights, and rooks, 1 queen and king like in real chess

#In chess if a pawn reaches the last row it can become a queen, this program will just handle it as a pawn unable to move.
    # queen_logic function would be rook_logic + a bishop_logic, bishop_logic sort of being rook_logic but in the style of calculating where pawns can attack, iterating steps in both directions at once


##Thoughts:
##Prefer having the board as a global variable over being a function. Feels like a game of hot potato between different functions.
#   That is how I did my tic tac toe program, but decided to try to approach this how the Sample Solution for tictactoe did things.