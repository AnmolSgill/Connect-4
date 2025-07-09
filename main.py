from environment import *

class Player:
    def __init__(self, name, piece):
        self.name = name # either CPU or player 1 or 2
        self.piece = piece # 1 or 2 / Red or Yellow


    def get_name(self):
        return self.name
    
    def get_piece(self):
        return self.piece


class Game:
    def __init__(self, grid):
        self.grid = grid
        self.connect = CONNECT_TARGET

        self._players = [
            Player('Player #1', PLAYER1_PIECE),
            Player('Player #2', PLAYER2_PIECE)
        ]


grid = Connect4Board(5, 5)
game = Game(grid)


player1 = game._players[0]
player2 = game._players[1]
print(player1.get_name())   # "Player #1"
print(player1.get_piece())  # 1
print(player2.get_name())   # "Player #2"
print(player2.get_piece())  # 2