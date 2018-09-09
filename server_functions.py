class ServerFunctions():

    def __init__(self, server_connection):
        self.server_connection = server_connection

    def create_game(self, name, player_id):
        command = {"command": "s_create_game", "params" : [name, player_id] }
        self.server_connection.send(command)    
        data = self.server_connection.receive()    
        if data[0] == "OK":
            return data[1]
        
    def get_games(self):
        command = {"command": "s_get_games", "params" : [] }
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK": 
            return data[1]
        elif data[0] == "EMPTY":
            return False

    def create_player(self, player_id, name):
        command = {"command": "s_create_player", "params" : [player_id, name] }
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return True
    
    def join_game(self, game_id, playerid):
        command = {'command': 's_join_game', 'params' : [game_id, playerid] }
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            print(data[1])
            return data[1]
        if data[0] == "ERROR":
            print(data[1])
            return False
    
    def get_game_status(self, game_id):
        command = {'command': 's_get_game_status', 'params' : [game_id]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return data[1]
        elif data[0] == "ERROR":
            return False
    
    def submit_board(self, game_id, player_id, board):
        command = {'command': 's_submit_board', 'params' : [game_id, player_id, board]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return True
        elif data[0] == "ERROR":
            return False

    def get_active_player(self, game_id):
        command = {'command': 's_get_active_player', 'params' : [game_id]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return data[1]
        elif data[0] == "ERROR":
            return False

    def get_round_data(self, game_id, player_id):
        command = {'command': 's_get_round_data', 'params' : [game_id, player_id]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return data[1]
        elif data[0] == "ERROR":
            return False
        
    def drop_bomb(self, game_id, player_id, row, col):
        command = {'command': 's_drop_bomb', 'params': [game_id, player_id, row, col] }
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return data[1]
        elif data[0] == "ERROR":
            return False
    
    def get_game_info(self, game_id):
        command = {'command': 's_get_game_info', 'params': [game_id]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return data[1]
        elif data[0] == "ERROR":
            return False

    def wait_for_game_status(self, game_id, status):
        command = {'command': 's_wait_for_game_status', 'params': [game_id, status]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return True
    
    def wait_for_turn(self, game_id, player_id):
        command = {'command': 's_wait_for_turn', 'params': [game_id, player_id]}
        self.server_connection.send(command)
        data = self.server_connection.receive()
        if data[0] == "OK":
            return True