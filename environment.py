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

        # Check positive Diagonal (/)
        count = 0
        r, c = row, col
        # Move to bottom left of board
        while r < self.rows - 1 and c > 0:
            r += 1
            c -= 1
        
        # Move from bottom left to top right
        while r >= 0 and c < self.columns:
            if self.grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT_TARGET:
                return True
            r -= 1
            c += 1
        
        # Check negative diagonal (\)
        count = 0
        r, c = row, col
        # Move to top left of board
        while r > 0 and c > 0:
            r -= 1
            c -= 1
        # Move from top left to bottom right
        while r < self.rows and c < self.columns:
            if self.grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == CONNECT_TARGET:
                return True
            r += 1
            c += 1
        return False
    

board = Connect4Board(columns = 4, rows = 4)
board.placePlayerPiece(2, 1)
board.placePlayerPiece(2, 1)
board.placePlayerPiece(3, 2)
row = board.placePlayerPiece(2,1)
board.placePlayerPiece(2,1)
if board.checkWin(CONNECT_TARGET, row, 2, 1):
    print("Player 1 wins")
board.printConnect4Board()

def test_horizontal_win():
    print("Testing horizontal win:")
    board = Connect4Board(columns=7, rows=6)
    
    # Place 4 horizontal pieces for Player 1 in bottom row (row = 5)
    for col in range(4):
        row = board.placePlayerPiece(col, PLAYER1_PIECE)

    board.printConnect4Board()
    win = board.checkWin(CONNECT_TARGET, row, 3, PLAYER1_PIECE)  # Check at last placed spot
    print("Passed" if win else "Failed")
    print()

def test_vertical_win():
    print("Testing vertical win:")
    board = Connect4Board(columns=7, rows=6)

    col = 2
    for _ in range(4):
        row = board.placePlayerPiece(col, PLAYER2_PIECE)

    board.printConnect4Board()
    win = board.checkWin(CONNECT_TARGET, row, col, PLAYER2_PIECE)
    print("Passed" if win else "Failed")
    print()

def test_positive_diagonal_win():
    print("Testing positive diagonal win (/):")
    board = Connect4Board(columns=7, rows=6)

    # Build the diagonal from bottom-left to top-right
    # build from (5,0) to (2,3)
    board.placePlayerPiece(0, PLAYER1_PIECE)  # row 5, col 0

    board.placePlayerPiece(1, PLAYER2_PIECE)
    board.placePlayerPiece(1, PLAYER1_PIECE)  # row 4, col 1

    board.placePlayerPiece(2, PLAYER2_PIECE)
    board.placePlayerPiece(2, PLAYER2_PIECE)
    board.placePlayerPiece(2, PLAYER1_PIECE)  # row 3, col 2

    board.placePlayerPiece(3, PLAYER2_PIECE)
    board.placePlayerPiece(3, PLAYER2_PIECE)
    board.placePlayerPiece(3, PLAYER2_PIECE)
    row = board.placePlayerPiece(3, PLAYER1_PIECE)  # row 2, col 3

    board.printConnect4Board()
    win = board.checkWin(CONNECT_TARGET, row, 3, PLAYER1_PIECE)
    print("Passed" if win else "Failed")
    print()

def test_negative_diagonal_win():
    print("Testing negative diagonal win (\\):")
    board = Connect4Board(columns=7, rows=6)

    # Build the diagonal from top-left to bottom-right
    # build from (2,0) to (5,3)
    board.placePlayerPiece(3, PLAYER1_PIECE)  # row 5, col 3

    board.placePlayerPiece(2, PLAYER2_PIECE)
    board.placePlayerPiece(2, PLAYER1_PIECE)  # row 4, col 2

    board.placePlayerPiece(1, PLAYER2_PIECE)
    board.placePlayerPiece(1, PLAYER2_PIECE)
    board.placePlayerPiece(1, PLAYER1_PIECE)  # row 3, col 1

    board.placePlayerPiece(0, PLAYER2_PIECE)
    board.placePlayerPiece(0, PLAYER2_PIECE)
    board.placePlayerPiece(0, PLAYER2_PIECE)
    row = board.placePlayerPiece(0, PLAYER1_PIECE)  # row 2, col 0

    board.printConnect4Board()
    win = board.checkWin(CONNECT_TARGET, row, 0, PLAYER1_PIECE)
    print("Passed" if win else "Failed")
    print()

# Run all tests
test_horizontal_win()
test_vertical_win()
test_positive_diagonal_win()
test_negative_diagonal_win()

