from settings import Settings
from game_session import GameSession
from text_color import *
settings = Settings()
session = GameSession("dsa-355", 1, settings)

def print_boards(session):
    print("Your board:            Enemy board:")
    rows = len(session.player_board)
    cols = len(session.player_board[0])
    for row in range(rows):
        print(str(chr(row + 65)),end=" ")
        for col in range(cols):
            grid = session.player_board[row][col]
            if session.player_board_hit_grid[row][col]:
                change_text_color("Red")
            if grid:
                print(session.player_board[row][col], end=" ")
            else:
                print(".", end=" ")
            change_text_color("Default")
        print("    ", end =" ")
        print(str(chr(row + 65)),end=" ")
        for col in range(cols):
            grid = session.enemy_board[row][col]
            if session.enemy_board_hit_grid[row][col]:
                change_text_color("Red")
            if grid:
                print(session.enemy_board[row][col], end=" ")
            else:
                print(".", end=" ")
            change_text_color("Default")
        print()
    print(end="  ")
    for x in range(cols):
        print(x + 1, end=" ")
    print("      ", end=" ")
    for x in range(cols):
        print(x + 1, end=" ")
    print()

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        print(str(chr(row + 65)),end=" ")
        for col in range(cols):
            grid = board[row][col]
            if grid:
                print(board[row][col], end=" ")
            else:
                print(".", end=" ")
        print()
    print(end="  ")
    for x in range(cols):
        print(x + 1, end=" ")
    print()

def print_ships():
    print("A A A A A : Aircraft Carrier")
    print("B B B B : Battle Ship")
    print("C C C : Cruiser")
    print("D D : Destroyer")
    print("S : Submarine")

def place_ship(row, col, alignment, shiptype, board, settings):
    rows = len(board)
    cols = len(board[0])

    shiplength = settings.shiplength[shiptype]
    if row > rows or col > cols:
        return False

    if alignment == "horizontal":
        if col + shiplength > cols:
            return False
        else:
            for x in range(shiplength):
                if board[row][col + x]:
                    return False
        for x in range(shiplength):
            board[row][col + x] = shiptype[0]
    
    if alignment == "vertical":
        if row + shiplength > rows:
            return False
        else:
            for y in range(shiplength):
                if board[row + y][col]:
                    return False
        for y in range(shiplength):
            board[row + y][col] = shiptype[0]
    return True

def coord_input(settings):
    while True:
        position = input("Target:")
        if len(position) != 2:
            print("Invalid input")
            continue
        try:    
            row = ord(position[0].upper()) - 65
            col = int(position[1]) -1
        except ValueError:
            print("Invalid input")
            continue
        else:
            if row > settings.rows - 1 or col > settings.cols - 1 or row < 0 or col < 0:
                print("Invalid input")
                continue
            break
    return (row, col)

def place_ships(session, settings):
    for shiptype, amount in settings.shiplist.items():
        for i in range(amount):
            placed = False
            while not placed:
                print_board(session.player_board)
                print_ships()
                coords = coord_input(settings)
                row = coords[0]
                col = coords[1]
                
                shiplength = settings.shiplength[shiptype]

                # Only lengthy ships needs alignement
                if shiplength > 1:
                    alignment = input("(V)ertical or (H)orizontal:")
                else:
                    alignment = "vertical"
                
                if alignment.lower() == "v" or alignment.lower() == "vertical":
                    alignment = "vertical"
                elif alignment.lower() == "h" or alignment.lower() == "horizontal":
                    alignment = "horizontal"
                placed = place_ship(row, col, alignment, shiptype, session.player_board, settings)
                if not placed:
                    print("Invalid position")

#print("\033[0;37;50m")
#place_ships(session, settings)
session.player_board_hit_grid[0][0] = True
session.enemy_board_hit_grid[3][3] = True
print_boards(session)
coords = coord_input(settings)
print(coords)