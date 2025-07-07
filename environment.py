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
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(EMPTY_SPACE)
            grid.append(row)
        return grid
    
    def placePlayerPiece(self, selectedColumn, playerPiece):
        if (selectedColumn < 0 or selectedColumn >= self.columns):
            print("OUT OF RANGE")
        else:
            rows = self.rows - 1
            for row in range(rows, -1, -1):
                if self.grid[row][selectedColumn] == EMPTY_SPACE:
                    self.grid[row][selectedColumn] = playerPiece
                    return row
    
    def printConnect4Board(self):
        for row in self.grid:
            print(row)
    
    def checkWin(self, CONNECT_Target, row, col, piece):

        # Check horizontal
        count = 0

        for c in range(self.columns):
            if self.grid[row][c] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT_TARGET:
                return True

        # Check Vertical
        count = 0
        for r in range(self.rows):
            if self.grid[r][col] == piece:
                count += 1
            else: 
                count = 0
            if count == CONNECT_TARGET:
                return True

        # Check Diagonal
    

board = Connect4Board(columns = 7, rows = 6)
board.placePlayerPiece(2, 1)
board.placePlayerPiece(3, 2)
board.printConnect4Board()
