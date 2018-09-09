#!/usr/bin/python3
import pickle
from server_connection import ServerConnection
from server_functions import ServerFunctions
from game_session import GameSession
from settings import Settings
from text_color import *

def select_game_menu(sf):
    # Query server for list of games
    games_list = sf.get_games()
    if games_list:
        for game in games_list:
            print(game)
        option = input("Select game id:")
        return option
    else:
        return False

def game_menu():
    print("Select an option:" )
    print("1. Select a game to join.")
    print("2. Create a new game.")
    option = input("Select:")
    return option

def input_player_name():
    player_name = input("Enter PlayerName:")
    return player_name

def game_creation(sf, player_id):
    while True:
        option = game_menu()
        # Join an existing game
        if option == "1":
            game_id = select_game_menu(sf)
            if game_id:
                if sf.join_game(int(game_id), player_id):
                    return game_id
                    
        # Create a new game
        elif option == "2":
            game_name = input("Enter GameName:")
            game_id = sf.create_game(game_name,player_id)
            return game_id
    
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
        
def place_ships(session, settings):
    for shiptype, amount in settings.shiplist.items():
        for i in range(amount):
            placed = False
            while not placed:
                print_board(session.player_board)
                print_ships()                
                print("Place " + shiptype + " x" + str(amount) + ":")
                coords = coord_input(settings)
                row = coords[0]
                col = coords[1]
                
                shiplength = settings.shiplength[shiptype]
                if shiplength > 1:
                    while True:
                        alignment = input("(V)ertical or (H)orizontal:")
                        if alignment.lower() == "v" or alignment.lower() == "vertical":
                            alignment = "vertical"
                            break
                        elif alignment.lower() == "h" or alignment.lower() == "horizontal":
                            alignment = "horizontal"
                        else:
                            print_in_color("Invalid input!", "Red")
                            continue
                        break
                else: # Only lengthy ships needs alignement
                    alignment = "vertical"
                placed = place_ship(row, col, alignment, shiptype, session.player_board, settings)
                if not placed:
                    print_in_color("Invalid position!", "Red")

def get_game_status(sf, session):
    current_status = sf.get_game_status(session.game_id)
    return current_status

def print_boards(session):
    """Print out player and enemy boards"""
    print("Your board:            Enemy board:")
    rows = len(session.player_board)
    cols = len(session.player_board[0])
    for row in range(rows):
        print(str(chr(row + 65)),end=" ")
        for col in range(cols):
            grid = session.player_board[row][col]
            if session.player_board_hit_grid[row][col]:
                change_text_color("Red")
                if session.rd_last_bomb_coords[0] == row and session.rd_last_bomb_coords[1] == col:
                    change_text_color(34)
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

def get_round_data(sf, session):
    """Retrieve the round data and populate session data"""
    data = sf.get_round_data(session.game_id, session.player_id)
    session.rd_last_bomb_coords = data[0]
    session.rd_game_status = data[1]

def process_round_data(session):
    
    if session.rd_last_bomb_coords:
        row = session.rd_last_bomb_coords[0]
        col = session.rd_last_bomb_coords[1]
        if not session.player_board_hit_grid[row][col]:
            # Place the strike on hit grid
            session.player_board_hit_grid[row][col] = True
            # Check if hit and if so enter it on the board
            if session.player_board[row][col]:
                print_in_color("Ouch! you got hit :(","Red")
                session.player_board[row][col] = "X"

    
    if session.rd_game_status == "finished":
        session.game_over = True
    
def drop_bomb(sf, session):
    while True:
        coords = coord_input(settings)
        row = coords[0]
        col = coords[1]
        # Check if grid is already bombed
        if session.enemy_board_hit_grid[row][col]:
            print_in_color("Grid already nuked", "Red")
        else:
            break

    result = sf.drop_bomb(session.game_id,session.player_id, row, col)
    session.enemy_board_hit_grid[row][col] = True
    if result == "HIT":
        session.enemy_board[row][col] = "X"
        print_in_color("It was hit! :)", "Green")
    else:
        print_in_color("You missed :(", "Red")

def coord_input(settings):
    """Prompt player to input coords, returns a tuple with row, col"""
    while True:
        position = input("Target:")
        if len(position) != 2:
            print("Invalid input")
            continue
        try:    
            row = ord(position[0].upper()) - 65
            col = int(position[1]) - 1
        except ValueError:
            print_in_color("Invalid input!", "Red")
            continue
        else:
            if row > settings.rows - 1 or col > settings.cols - 1 or row < 0 or col < 0:
                print_in_color("Invalid input!", "Red")
                continue
            break
    return (row, col)

def retrieve_game_info(sf, session):
    game_info = sf.get_game_info(session.game_id)
    session.game_name = game_info[0]
    players = game_info[1]
    for player in players:
        if player[0] != session.player_id:
            session.opponent_name = player[1]

def connect_to_host(server_connection):
    """Prompts for host/ip and tries to connect"""
    default_host = "94.254.80.160" # My Pi3 @ home
    default_port = 8745
    print("Enter host/ip:port of server to connect to or leave blank for default (" + default_host + ":" + str(default_port) + ")")
    while True:
        while True:
            hostandport = input("Enter host:")
            if hostandport == "":
                host = default_host
                port = default_port
            else:
                hostandport = hostandport.split(":")
                host = hostandport[0]
                if len(hostandport) == 1:
                    port = default_port
                elif len(hostandport) == 2:
                    try:
                        port = int(hostandport[1])
                    except ValueError:
                        print_in_color("Invalid port number!", "Red")
                        continue
                else:
                    print_in_color("Invalid input! format should be [host/ip]:[port]", "Red")
                    continue
            break

        if server_connection.connect(host, port):
            break

# Connect to server
server_connection = ServerConnection()
connect_to_host(server_connection)

# Instantiate Settings and ServerFunctions
settings = Settings()
sf = ServerFunctions(server_connection)

# Ask for a player name and store it
player_name = input_player_name()

# Retrieve uuid
player_id = settings.get_uuid()

# Create Player and Game on Server
sf.create_player(player_id, player_name)
game_id = game_creation(sf, player_id)
session = GameSession(player_id, game_id, settings)
session.player_name = player_name

# Wait for another player to join
print("Waiting for opponent")
#wait_for_status(sf, session, "preparing")
sf.wait_for_game_status(session.game_id, "preparing")
retrieve_game_info(sf, session)
print(session.game_name + " is starting!")
print(session.player_name + " vs " + session.opponent_name)


# Place ships and submit the board to server
place_ships(session, settings)
sf.submit_board(session.game_id, session.player_id, session.player_board)

# Wait for other player to place ships
print("Waiting for " + session.opponent_name + " to place ships.")
#wait_for_status(sf, session, "running")
sf.wait_for_game_status(session.game_id, "running")
# Game Loop
while True:
    if sf.get_active_player(session.game_id) != session.player_id:
        print_boards(session)
        print("Waiting for " + session.opponent_name + "...")
        #wait_for_turn(sf, session)
        sf.wait_for_turn(session.game_id, session.player_id)
    get_round_data(sf, session)
    process_round_data(session)
    if session.game_over: # You lost
        print("You lost ;(")
        break
    print_boards(session)
    drop_bomb(sf, session)
    get_round_data(sf, session)
    process_round_data(session)
    if session.game_over: # You win
        print("You win! xD")
        break
