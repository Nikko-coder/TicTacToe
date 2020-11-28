# Author: Nikola Ticha
import random


# colors for game
class Color:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


# set-up
winner = None  # nobody won
game_mode = True  # game is played, nobody won or lost yet
x = Color.PURPLE + Color.BOLD + "X" + Color.END
y = Color.BLUE + Color.BOLD + "O" + Color.END
current_player = x
pc = y  # for single player regime


# board, stepwise filled up with game stones:
board = [" ", " ", " ",
         " ", " ", " ",
         " ", " ", " "]


# updated board with inputs from board[]
def play_area():
    print("-" * 14)
    print(board[6] + "  |  " + board[7] + "  |  " + board[8])
    print("-" * 14)
    print(board[3] + "  |  " + board[4] + "  |  " + board[5])
    print("-" * 14)
    print(board[0] + "  |  " + board[1] + "  |  " + board[2])
    print("-" * 14)


# C: Functions involved in the game - for SINGLE PLAYER - describing pc moves
# function for switching players in single player regime
def pc_switch_player():
    global current_player, x, y, pc
    if current_player == x:
        pc = y
    else:
        pc = x


# checking for a win
def pc_win(board, m):
    return ((board[0] == board[1] == board[2] == m) or
            (board[3] == board[4] == board[5] == m) or
            (board[6] == board[7] == board[8] == m) or
            (board[0] == board[3] == board[6] == m) or
            (board[1] == board[4] == board[7] == m) or
            (board[2] == board[5] == board[8] == m) or
            (board[0] == board[4] == board[8] == m) or
            (board[2] == board[4] == board[6] == m))


# Making a duplicate for checking moves
def pc_get_board(board):
    duplicate = []
    for j in board:
        duplicate.append(j)
    return duplicate


# Checking moves
def pc_test_win(board, mark, i):
    b_copy = pc_get_board(board)
    b_copy[i] = mark
    return pc_win(b_copy, mark)


# Deciding move
def pc_computer_move():
    global current_player, pc
    # check if pc can win
    for i in range(0, 9):
        if board[i] == " " and pc_test_win(board, pc, i):
            return i
    # check if player can win
    for i in range(0, 9):
        if board[i] == " " and pc_test_win(board, current_player, i):
            return i
    # play corners
    for i in range(0, 9):
        if board[i] == " ":
            return i
    # play middle
    if board[4] == " ":
        return 4
    # play lines
    for i in [1, 3, 5, 7]:
        if board[i] == " ":
            return i
    else:
        return None


# pc move
def pc_make_move(player):
    while " " in board:
        print("It's the computer's turn: ")
        position = pc_computer_move()
        board[position] = player
        break
    play_area()


# B: Functions involved in the game - for MULTIPLAYER
# function asking for the position to place stone, checking free space and allowed number
def make_move(player):
    position = int(input("Please enter a position between 1-9: ")) - 1
    while position in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        if free_space(board, position):
            board[position] = player
        else:
            position = int(input("Please enter a position between only 1-9: ")) - 1
            if free_space(board, position):
                board[position] = player
        break
    else:
        position = int(input("Please enter a position between only 1-9: ")) - 1
        if free_space(board, position):
            board[position] = player
    play_area()


# function checking whether space for stone is already taken
def free_space(board, position):
    if board[position] == " ":
        return True


# function for switching players
def switch_player():
    global current_player, x, y
    if current_player == x:
        current_player = y
    else:
        current_player = x


# function checking for winner
def game_won():
    global winner
    row_winner = check_rows()
    column_winner = check_columns()
    diagonal_winner = check_diagonals()
    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    else:
        winner = None


# check rows
def check_rows():
    global game_mode
    row_1 = board[6] == board[7] == board[8] != " "
    row_2 = board[3] == board[4] == board[5] != " "
    row_3 = board[0] == board[1] == board[2] != " "

    if row_1 or row_2 or row_3:
        game_mode = False
    if row_1:
        return board[0]
    elif row_2:
        return board[3]
    elif row_3:
        return board[6]
    else:
        return None


# check columns
def check_columns():
    global game_mode
    column_1 = board[6] == board[3] == board[0] != " "
    column_2 = board[7] == board[4] == board[1] != " "
    column_3 = board[8] == board[5] == board[2] != " "
    if column_1 or column_2 or column_3:
        game_mode = False
    if column_1:
        return board[6]
    elif column_2:
        return board[7]
    elif column_3:
        return board[8]
    else:
        return None


# check diagonals
def check_diagonals():
    global game_mode
    diag_1 = board[8] == board[4] == board[0] != " "
    diag_2 = board[6] == board[4] == board[2] != " "
    if diag_1 or diag_2:
        game_mode = False
    if diag_1:
        return board[8]
    if diag_2:
        return board[6]
    else:
        return None


# function checking if game drawn
def game_drawn():
    global game_mode
    if " " not in board:
        game_mode = False
        return True
    else:
        return False


# A:Functions not directly involved in the game
# Choose letter to ensure that the correct stone is picked
def choice(letter):
    while not (letter == "X" or letter == "O"):
        letter = input("Choose X or O only:").upper()
    return letter


# who starts first
def start():
    global current_player
    if random.randint(0, 1) == 0:
        current_player = x
        return print("The game starts 'X' :")
    else:
        current_player = y
        return print("The game starts 'O' :")


# asking for a next game
def again():
    new_game = input("Do you want to play another game? (yes or no): ").lower()
    if new_game == "yes":
        return True


# Function containing functions for game - MULTIPLAYER
def mp_game_start():
    play_area()
    while game_mode:
        # making move
        make_move(current_player)
        # checking if win
        game_won()
        # checking if tie
        game_drawn()
        # switching player
        switch_player()
    if winner == x or winner == y:
        p = Color.YELLOW + "\U0001F3C6" + Color.END
        print(p + f" Congrats! The winner is {winner}! " + p)
    else:
        print("Game drawn X:O !")


# Function containing functions for game - SINGLE PLAYER
def sp_game_start():
    play_area()
    while game_mode:
        pc_switch_player()
        # making move
        make_move(current_player)
        # checking if win
        game_won()
        # checking if tie
        game_drawn()
        # switching player
        pc_make_move(pc)
        # checking if win
        game_won()
        # checking if tie
        game_drawn()
    if winner == x or winner == y:
        p = Color.YELLOW + "\U0001F3C6" + Color.END
        print(f"{p} Congrats! The winner is {winner}! {p}")
        if winner != current_player:
            print("What a shame! The computer beat you!")
        else:
            name = input("Please enter your name: ")

    else:
        print("Game drawn X:O !")


# Function for introduction - MP
def mp_intro():
    letter = input("Please choose 'X' or 'O': (enter X or O) ").upper()
    choice(letter)
    start()


# Function for introduction - SP
def sp_intro():
    global current_player, pc, x, y
    letter = input("Please choose 'X' or 'O': (enter X or O) ").upper()
    if letter == "X":
        current_player = x
        pc = y
    if letter == "O":
        current_player = y
        pc = x


def intro():
    print("\U0001F3C1" + Color.RED + " Welcome to TIC TAC TOE! " + Color.END + "\U0001F3C1")
    print(Color.RED + "GAME RULES:" + Color.END + """ Each player can place his stone per turn on the 3x3 grid. 
    The Winner is who succeeds in placing three of his stones in:
    * horizontal,
    * vertical or
    * diagonal row.
    ! Hint: Use your keyboard's number pad for entering the positions.""")


# Function clearing parameters for a new play
def clear():
    global winner, game_mode, current_player, pc, board
    winner = None  # nobody won
    game_mode = True  # game is played, nobody won or lost yet
    current_player = x
    pc = y

    # board, stepwise filled up with game stones:
    board = [" ", " ", " ",
             " ", " ", " ",
             " ", " ", " "]


def single_player():
    sp_intro()
    sp_game_start()


def multi_player():
    mp_intro()
    mp_game_start()


# Finally souhrn dila uff..
intro()
regime = input("Please enter 'S' for single player (you against the computer) or 'M' for multiplayer regime: ").upper()
try:
    if regime == "S":
        single_player()
        while again():
            clear()
            single_player()
    elif regime == "M":
        multi_player()
        while again():
            clear()
            multi_player()
finally:
    print("Goodbye!")
