from environment import *

class Player:
    def __init__(self, name, piece):
        self.name = name # either CPU or player 1 or 2
        self.piece = piece # 1 or 2 / Red or Yellow

    def getName(self):
        return self.name
    
    def getPiece(self):
        return self.piece


class Game:
    def __init__(self, grid):
        self.grid = grid
        self.connect = CONNECT_TARGET

        self.players = [
            Player('Player #1', PLAYER1_PIECE),
            Player('Player #2', PLAYER2_PIECE)
        ]
    
    def printConnect4Board(self):
        grid = self.grid.getGrid()
        for row in grid:
            print(row)

    def simulatePlayerMove(self, player):
        self.printConnect4Board()
        print("\n")
        chosenColumn = int(input(f"{player.getName()}'s turn, enter a column from 0 to {self.grid.getColumns() - 1}: "))
        placePiece = self.grid.placePlayerPiece(chosenColumn, player.getPiece())
        return placePiece

    def playRounds(self):
        winner = False
        while not winner:
            for p in self.players:
                placePiece = self.simulatePlayerMove(p)
                if self.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    return p

    def gameplay(self):
        gameWinner = self.playRounds()
        self.printConnect4Board()
        print("\n")
        print("================================================================")
        print(f"Congratulations {gameWinner.getName()}! You have won Connect-4!")
        print("================================================================")
        print("\n")

grid = Connect4Board(6, 7)
game = Game(grid)
game.gameplay()