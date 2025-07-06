from environment import *

class Player:
    def __init__(self, name, piece):
        self.name = name # either CPU or player 1 or 2
        self.piece = piece # 1 or 2 / Red or Yellow

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
game.play()
