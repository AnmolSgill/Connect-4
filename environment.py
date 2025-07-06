EMPTY_SPACE = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
CONNECT_TARGET = 4

class Connect4Board:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.grid = self.gridMaker()

    def gridMaker(self):
        print()