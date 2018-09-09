class GameSession():
    
    def __init__(self, player_id, game_id, settings):
    
        self.player_id = player_id
        self.game_id = game_id
        self.game_name = ""
        self.player_board = self.create_empty_board(settings)
        self.enemy_board = self.create_empty_board(settings)
        self.player_board_hit_grid = self.create_empty_hit_grid(settings)
        self.enemy_board_hit_grid = self.create_empty_hit_grid(settings)
        self.player_name = ""
        self.game_over = False

        self.opponent_name = ""
        
        # Data to be retrieved each round
        self.rd_last_bomb_coords = ()
        self.rd_game_status = ""


    def create_empty_board(self, settings):
        board = []
        for i in range(settings.rows):
            row = []
            for i in range(settings.cols):
                row.append("")
            board.append(row)
        return board

    def create_empty_hit_grid(self, settings):
        hit_grid = []
        for i in range(settings.rows):
            row = []
            for i in range(settings.cols):
                row.append(False)
            hit_grid.append(row)
        return hit_grid