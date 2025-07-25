from environment import *
from minimax import AdversarialSearch
from gemini_agent import GeminiAgent

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
        while True:
            try:
                column = int(input(f"{player.getName()}'s turn (0 to {self.grid.getColumns() - 1}): "))
                placed = self.grid.placePlayerPiece(column, player.getPiece())
                if placed is not None:
                    return
            except ValueError:
                print("Invalid input. Try again.")

def setup_game(rows, columns):
    grid = Connect4Board(columns, rows)
    game = Game(grid)
    return grid, game

def run_game(player1_strategy, player2_strategy, rows, columns):
    grid, game = setup_game(rows, columns)
    turn = 0
    winner = False

    while not winner:
        for p in game.players:
            strategy = player1_strategy if p.getPiece() == PLAYER1_PIECE else player2_strategy
            move = strategy(game, grid, p, turn)
            grid.placePlayerPiece(move, p.getPiece()) if move is not None else None
            if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                game.printConnect4Board()
                print(f"\n{p.getName()} wins!")
                winner = True
                break
            turn += 1

def human_strategy(game, grid, player, turn):
    game.simulatePlayerMove(player)
    return None

def gemini_strategy(difficulty):
    agent = GeminiAgent(player_piece=2, difficulty=difficulty)
    def strategy(game, grid, player, turn):
        return agent.choose_move(grid.getGrid())
    return strategy

def ai_strategy(algorithm):
    def strategy(game, grid, player, turn):
        ai = AdversarialSearch(grid.getRow(), grid.getColumns())
        if algorithm == "minimax":
            _, move, _ = ai.minimax(grid.getGrid(), 6, True)
        elif algorithm == "alphabeta":
            _, move, _ = ai.alphaBetaPruning(grid.getGrid(), 6, -999999999, 999999999, True, [])
        elif algorithm == "expectiminimax":
            _, move, _ = ai.expectiminiMax(grid.getGrid(), 6, True, turn)
        else:
            raise ValueError("Invalid AI algorithm")
        return move
    return strategy

def main_menu():
    print("Select Game Mode:")
    print("1 - Player vs Minimax")
    print("2 - Player vs Alpha-Beta")
    print("3 - Player vs Expectiminimax")
    print("4 - Player vs Gemini")
    print("5 - Gemini vs Minimax")
    print("6 - Gemini vs Alpha-Beta")
    print("7 - Gemini vs Expectiminimax")

    choice = input("Enter choice (1–7): ").strip()

    if choice in {"1", "2", "3"}:
        algo = {"1": "minimax", "2": "alphabeta", "3": "expectiminimax"}[choice]
        run_game(human_strategy, ai_strategy(algo), 6, 7)
    elif choice == "4":
        difficulty = input("Gemini difficulty (easy / medium / hard): ").strip().lower()
        run_game(human_strategy, gemini_strategy(difficulty), 6, 7)
    elif choice in {"5", "6", "7"}:
        difficulty = input("Gemini difficulty (easy / medium / hard): ").strip().lower()
        algo = {"5": "minimax", "6": "alphabeta", "7": "expectiminimax"}[choice]
        run_game(gemini_strategy(difficulty), ai_strategy(algo), 6, 7)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
