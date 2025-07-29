from environment import *
from minimax import AdversarialSearch
from gemini_agent import GeminiAgent
from random import randint

#player class defines a Player object with their name and piece
class Player:
    def __init__(self, name, piece):
        self.name = name # either CPU or player 1 or 2
        self.piece = piece # 1 or 2 / Red or Yellow

    def getName(self):
        return self.name
    
    def getPiece(self):
        return self.piece

#the game class defines an object with the connect 4 grid, the target (default 4), and players
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

#creates a game environment that agents/players will use
def setup_game(rows, columns):
    grid = Connect4Board(columns, rows)
    game = Game(grid)
    
    return grid, game

#simulates a game between gemini/human vs an adversarial agent
def run_game_vs_agent(player1_strategy, player2_strategy, rows, columns,algo):
    grid, game = setup_game(rows, columns)
    turn = 1
    winner = False
    visits = 0
    
    adversary = AdversarialSearch(rows,columns)

    #determines the algorithm to be used by the agent
    #if expectiminimax is chosen, the game incorporates randomness
    #if alphabeta is chosen, the game keeps track of the number of pruned branches

    if algo == "expectiminimax":
        while not winner:     
            for p in game.players:
                
                #checks to see if the game is in a tie state, no valid moves remaining and no winners
                if len(adversary.getValidMoves(grid.getGrid())) == 0:
                    print(f"Tie Game!")
                    print(f"Visited Nodes: {visits}")
                    return

                #randomness is injected by randomly selecting a move from all valid move every other turn for each player
                if p.getPiece() == PLAYER1_PIECE:

                    if turn % 4 == 3:
                        moves = adversary.getValidMoves(grid.getGrid())
                        i = randint(0,len(moves)-1)
                        grid.placePlayerPiece(moves[i],p.getPiece())

                    else:
                        strategy = player1_strategy
                        move = strategy(game, grid, p, turn)

                else:

                    if turn % 4 == 0:
                        moves = adversary.getValidMoves(grid.getGrid())
                        i = randint(0,len(moves)-1)
                        grid.placePlayerPiece(moves[i],p.getPiece())
                    
                    else:

                        strategy = player2_strategy
                        move,visited = strategy(game, grid, p, turn)
                        visits += visited 
                        grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                #after every move, determines if a player has won
                if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    game.printConnect4Board()
                    print(f"\n{p.getName()} wins!")
                    winner = True
                    print(f"Visited Nodes: {visits}")

                    return visits

                turn +=1 
                
                

                
    
    if algo == "alphabeta":
        pruned = []

        while not winner:     
            for p in game.players:

                #checks to see if the game is in a tie state, no valid moves remaining and no winners
                if len(adversary.getValidMoves(grid.getGrid())) == 0:
                    print(f"Tie Game!")
                    print(f"Visited Nodes: {visits} \nPruned Nodes: {len(pruned)}")
                    
                    return

                if p.getPiece() == PLAYER1_PIECE:

                    
                    strategy = player1_strategy
                    move = strategy(game, grid, p, turn)

                else:


                    strategy = player2_strategy
                    move,visited = strategy(game, grid, p, turn, pruned)
                    visits += visited 
                    grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                #after every move, determines if a player has won
                if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    game.printConnect4Board()
                    print(f"\n{p.getName()} wins!")
                    winner = True
                    print(f"Visited Nodes: {visits} \nPruned Nodes: {len(pruned)}")
                    return 
                
                turn += 1
                
    
    if algo == "minimax":
        while not winner:     
            for p in game.players:

                #checks to see if the game is in a tie state, no valid moves remaining and no winners
                if len(adversary.getValidMoves(grid.getGrid())) == 0:
                    print(f"Tie Game!")
                    print(f"Visited Nodes: {visits}")
                    return

                if p.getPiece() == PLAYER1_PIECE:

                    
                    strategy = player1_strategy
                    move = strategy(game, grid, p, turn)

                else:

                    strategy = player2_strategy
                    move,visited = strategy(game, grid, p, turn)
                    visits += visited 
                    grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                #after every move, determines if a player has won
                if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    game.printConnect4Board()
                    print(f"\n{p.getName()} wins!")
                    winner = True
                    print(f"Visited Nodes: {visits}")
                    return 

                turn += 1
                
            
#simulates a game between two adversarial agents
def run_agent_vs_agent(player1_strategy, player2_strategy, rows, columns,algo):
    grid, game = setup_game(rows, columns)
    turn = 1
    winner = False
    visits = 0
    
    adversary = AdversarialSearch(rows,columns)
    game.printConnect4Board()

    if algo == "expectiminimax":
        while not winner:     
            for p in game.players:

                #checks to see if the game is in a tie state, no valid moves remaining and no winners

                if len(adversary.getValidMoves(grid.getGrid())) == 0:
                    print(f"Tie Game!")
                    print(f"Visited Nodes: {visits}")
                    return

                #randomness is injected by randomly selecting a move from all valid move every other turn for each player

                if p.getPiece() == PLAYER1_PIECE:

                    if turn % 4 == 3:
                        moves = adversary.getValidMoves(grid.getGrid())
                        i = randint(0,len(moves)-1)
                        grid.placePlayerPiece(moves[i],p.getPiece())

                    else:
                        strategy = player1_strategy
                        move,visited = strategy(game, grid, p, turn)
                        visits += visited 
                        grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                else:

                    if turn % 4 == 0:
                        moves = adversary.getValidMoves(grid.getGrid())
                        i = randint(0,len(moves)-1)
                        grid.placePlayerPiece(moves[i],p.getPiece())
                    
                    else:

                        strategy = player2_strategy
                        move,visited = strategy(game, grid, p, turn)
                        visits += visited 
                        grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                #after every move, determines if a player has won

                if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    game.printConnect4Board()
                    print(f"\n{p.getName()} wins!")
                    winner = True
                    print(f"Visited Nodes: {visits}")

                    return visits

                turn +=1 
                
                

                
    
    if algo == "alphabeta":
        pruned = []

        while not winner:
                 
            for p in game.players:

                #checks to see if the game is in a tie state, no valid moves remaining and no winners

                if len(adversary.getValidMoves(grid.getGrid())) == 0:
                    game.printConnect4Board()
                    print(f"Tie Game!")
                    print(f"Visited Nodes: {visits} \nPruned Nodes: {len(pruned)}")
                    
                    return

                if p.getPiece() == PLAYER1_PIECE:

                    
                    strategy = player1_strategy
                    
                    move,visited = strategy(game, grid, p, turn, pruned)
                    visits += visited 
                    grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                else:


                    strategy = player2_strategy
                    move,visited = strategy(game, grid, p, turn, pruned)
                    visits += visited 
                    grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                #after every move, determines if a player has won

                if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    game.printConnect4Board()
                    print(f"\n{p.getName()} wins!")
                    winner = True
                    print(f"Visited Nodes: {visits} \nPruned Nodes: {len(pruned)}")
                    return 
                
                turn += 1
                game.printConnect4Board()
                
    
    if algo == "minimax":
        while not winner:     
            for p in game.players:

                #checks to see if the game is in a tie state, no valid moves remaining and no winners

                if len(adversary.getValidMoves(grid.getGrid())) == 0:
                    print(f"Tie Game!")
                    print(f"Visited Nodes: {visits}")
                    return

                if p.getPiece() == PLAYER1_PIECE:

                    
                    strategy = player1_strategy
                    
                    move,visited = strategy(game, grid, p, turn)
                    visits += visited 
                    grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                else:

                    strategy = player2_strategy
                    move,visited = strategy(game, grid, p, turn)
                    visits += visited 
                    grid.placePlayerPiece(move, p.getPiece()) if move is not None else None

                #after every move, determines if a player has won

                if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    game.printConnect4Board()
                    print(f"\n{p.getName()} wins!")
                    winner = True
                    print(f"Visited Nodes: {visits}")
                    return 

                turn += 1            
        
    

#simulates a game between a human and gemini
def run_game(player1_strategy, player2_strategy, rows, columns):
    grid, game = setup_game(rows, columns)
    turn = 1
    winner = False


    while not winner:
        for p in game.players:

            if p.getPiece() == PLAYER1_PIECE:

                strategy = player1_strategy
                move = strategy(game, grid, p, turn)

            else:
                strategy = player2_strategy
                move = strategy(game, grid, p, turn)

            grid.placePlayerPiece(move, p.getPiece()) if move is not None else None
            
            
            #after every move, determines if a player has won
            if grid.checkWin(CONNECT_TARGET, p.getPiece()):
                game.printConnect4Board()
                print(f"\n{p.getName()} wins!")
                winner = True
                break

            turn += 1

#the human strategy prompts a player to select a column 
def human_strategy(game, grid, player, turn):
    game.simulatePlayerMove(player)

    
    return 

#the gemini strategy sends a prompt to the API based on the chosen difficulty
def gemini_strategy(difficulty):
    agent = GeminiAgent(player_piece=2, difficulty=difficulty)
    def strategy(game, grid, player, turn):
        return agent.choose_move(grid.getGrid())
    
    
    return strategy

#the AI strategy runs an adversarial search algorithm depending on the chosen game mode
def ai_strategy(algorithm):
    def strategy(game, grid, player, turn, pruned = None):
        if player.getPiece() == 1:
            opponent = 2
        else:
            opponent = 1

        ai = AdversarialSearch(grid.getRow(), grid.getColumns())
        if algorithm == "minimax":
            _, move, visited = ai.minimax(grid.getGrid(), 6, True,player.getPiece(),opponent)
        elif algorithm == "alphabeta":
            
            _, move, visited = ai.alphaBetaPruning(grid.getGrid(), 6, -999999999, 999999999, True,player.getPiece(),opponent, pruned)
            return move,visited
        elif algorithm == "expectiminimax":
            _, move, visited = ai.expectiminiMax(grid.getGrid(), 6, True, turn,player.getPiece(),opponent)
        else:
            raise ValueError("Invalid AI algorithm")
        
        
        return move, visited
    
    
    return strategy

#command line prompt version, use keys to select game mode
def main_menu():
    print("Select Game Mode:")
    print("1 - Player vs Minimax")
    print("2 - Player vs Alpha-Beta")
    print("3 - Player vs Expectiminimax")
    print("4 - Player vs Gemini")
    print("5 - Gemini vs Minimax")
    print("6 - Gemini vs Alpha-Beta")
    print("7 - Gemini vs Expectiminimax")
    print("8 - Minimax vs Minimax")
    print("9 - Alpha-Beta vs Alpha-Beta")
    print("0 - Expectiminimax vs Expectiminimax")

    choice = input("Enter choice (1–7): ").strip()

    if choice in {"1", "2", "3"}:
        algo = {"1": "minimax", "2": "alphabeta", "3": "expectiminimax"}[choice]
        run_game_vs_agent(human_strategy, ai_strategy(algo), 6, 7,algo)
    elif choice == "4":
        difficulty = input("Gemini difficulty (easy / medium / hard): ").strip().lower()
        run_game(human_strategy, gemini_strategy(difficulty), 6, 7)
    elif choice in {"5", "6", "7"}:
        difficulty = input("Gemini difficulty (easy / medium / hard): ").strip().lower()
        algo = {"5": "minimax", "6": "alphabeta", "7": "expectiminimax"}[choice]
        run_game_vs_agent(gemini_strategy(difficulty), ai_strategy(algo), 6, 7,algo)
    elif choice in {"8","9","0"}:
        algo = {"8": "minimax", "9": "alphabeta", "0": "expectiminimax"}[choice]
        run_agent_vs_agent(ai_strategy(algo), ai_strategy(algo), 6, 7,algo)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
