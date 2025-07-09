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
    
    def checkWin(self, CONNECT_TARGET, piece):
        
        # check all directions for each cell (Horizontal, vertical, both diagonals)
        for row in range(self.rows):
            for col in range(self.columns):

                #skip if current cell does not match player's piece
                if self.grid[row][col] != piece:
                    continue

                # horiztonal - right
                if col + CONNECT_TARGET <= self.columns:
                    if all(self.grid[row][col + i] == piece for i in range(CONNECT_TARGET)):
                        return True
                    
                # veritcal down
                if row + CONNECT_TARGET <= self.rows:
                    if all(self.grid[row + i][col] == piece for i in range(CONNECT_TARGET)):
                        return True
                    
                # Diagonal down-right (negative slope) \
                if row + CONNECT_TARGET <= self.rows and col + CONNECT_TARGET <= self.columns:
                    if all(self.grid[row + i][col + i] == piece for i in range(CONNECT_TARGET)):
                        return True
                
                # diaganol up right (positive slope) /
                if row - CONNECT_TARGET + 1 >= 0 and col + CONNECT_TARGET <= self.columns:
                    if all(self.grid[row - i][col + i] == piece for i in range (CONNECT_TARGET)):
                        return True
        
        return False


