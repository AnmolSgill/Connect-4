import pygame
import sys
from main import setup_game, human_strategy, ai_strategy, gemini_strategy
from environment import PLAYER1_PIECE, PLAYER2_PIECE, EMPTY_SPACE, CONNECT_TARGET
from minimax import AdversarialSearch
from random import randint

#constants for graphical display
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

#RGB color definitions
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#initialize pygame and fonts
pygame.init()
FONT = pygame.font.SysFont("monospace", 40)
SMALL_FONT = pygame.font.SysFont("monospace", 30)

#draws the current game board on the screen with optional messages
def draw_board(screen, grid_obj, rows, cols, message=""):
    grid = grid_obj.getGrid()
    screen.fill(BLACK)
    for c in range(cols):
        for r in range(rows):
            #draw the board background grid
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            #determine piece colour for each cell
            color = BLACK
            if grid[r][c] == PLAYER1_PIECE:
                color = RED
            elif grid[r][c] == PLAYER2_PIECE:
                color = YELLOW
            #draw the circle for each piece
            pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    #display optional message at the top
    if message:
        label = SMALL_FONT.render(message, 1, WHITE)
        screen.blit(label, (10, 10))

    pygame.display.update()

#display the game mode selection menu
def show_menu(screen, height):
    options = [
        "1 - Player vs Minimax",
        "2 - Player vs Alpha-Beta",
        "3 - Player vs Expectiminimax",
        "4 - Player vs Gemini",
        "5 - Gemini vs Minimax",
        "6 - Gemini vs Alpha-Beta",
        "7 - Gemini vs Expectiminimax",
        "8 - Minimax vs Minimax",
        "9 - Alpha-Beta vs Alpha-Beta",
        "0 - Expectiminimax vs Expectiminimax"
    ]

    menu_font = pygame.font.SysFont("monospace", 30)
    selected_idx = -1
    spacing = 40
    top_margin = (height - len(options) * spacing) // 2

    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        #render each menu option and detect mouse hover
        for i, option in enumerate(options):
            color = YELLOW if i == selected_idx else WHITE
            text = menu_font.render(option, True, color)
            rect = text.get_rect(topleft=(60, top_margin + i * spacing))
            screen.blit(text, rect)

            if rect.collidepoint(mouse_pos):
                selected_idx = i

        pygame.display.update()

        #return selected option on mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and selected_idx != -1:
                return selected_idx + 1

#menu to select Gemini difficulty
def select_difficulty(screen, height):
    difficulties = ["easy", "medium", "hard"]
    selected_idx = -1
    spacing = 50
    menu_font = pygame.font.SysFont("monospace", 30)
    title_font = pygame.font.SysFont("monospace", 36)
    top_margin = (height - len(difficulties) * spacing) // 2

    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        title = title_font.render("Select Gemini Difficulty", True, WHITE)
        screen.blit(title, (60, 40))

        #display difficulty options
        for i, diff in enumerate(difficulties):
            color = YELLOW if i == selected_idx else WHITE
            text = menu_font.render(diff.capitalize(), True, color)
            rect = text.get_rect(topleft=(60, top_margin + i * spacing))
            screen.blit(text, rect)

            if rect.collidepoint(mouse_pos):
                selected_idx = i

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and selected_idx != -1:
                return difficulties[selected_idx]

#main deterministic game loop (used for minimax, alpha-beta, gemini)
def gui_game(player1_tuple, player2_tuple, rows, cols):
    player1_strategy, player1_label = player1_tuple
    player2_strategy, player2_label = player2_tuple

    grid, game = setup_game(rows, cols)
    width = cols * SQUARESIZE
    height = (rows + 2) * SQUARESIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect-4 AI Game")

    turn = 1
    game_over = False
    pruned = []
    draw_board(screen, grid, rows, cols, "Game Start!")

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    #Determine who's turn and which strategy to use
        current_player = PLAYER1_PIECE if turn % 2 == 1 else PLAYER2_PIECE
        strategy = player1_strategy if current_player == PLAYER1_PIECE else player2_strategy
        label = player1_label if current_player == PLAYER1_PIECE else player2_label
        player_name = f"Player {1 if current_player == PLAYER1_PIECE else 2}"
        player = game.players[0] if turn%2 == 1 else game.players[1]

        if strategy == human_strategy:
            #human turn: wait for mouse click
            draw_board(screen, grid, rows, cols, f"{player_name}'s Turn (You)")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(posx / SQUARESIZE)
                    #check win or tie
                    if grid.getGrid()[0][col] == EMPTY_SPACE:
                        grid.placePlayerPiece(col, current_player)
                        if grid.checkWin(CONNECT_TARGET, current_player):
                            if len(pruned)> 0:
                                draw_board(screen, grid, rows, cols, f"{player_name} wins! Pruned: {len(pruned)}")
                            else:
                                draw_board(screen, grid, rows, cols, f"{player_name} wins!")
                            
                            game_over = True
                        elif not any(EMPTY_SPACE in row for row in grid.getGrid()):
                            if len(pruned)> 0:
                                draw_board(screen, grid, rows, cols, f"Tie Game! Pruned: {len(pruned)}")
                            else:
                                draw_board(screen, grid, rows, cols, "Tie Game!")
                            game_over = True
                        else:
                            draw_board(screen, grid, rows, cols, "")
                        turn += 1
        else:
            #AI turn: delay then call strategy function
            draw_board(screen, grid, rows, cols, f"{player_name}'s Turn ({label})")
            pygame.time.wait(800)
            if label == "Alpha-Beta":
                result = strategy(game, grid, player, turn,pruned)
            else:
                result = strategy(game, grid, player, turn)

            move = result if isinstance(result, int) else result[0]
            if move is not None and grid.getGrid()[0][move] == EMPTY_SPACE:
                grid.placePlayerPiece(move, current_player)
                if grid.checkWin(CONNECT_TARGET, current_player):
                    if len(pruned)> 0:
                        draw_board(screen, grid, rows, cols, f"{player_name} wins! Pruned: {len(pruned)}")
                    else:
                        draw_board(screen, grid, rows, cols, f"{player_name} wins!")
                    game_over = True
                elif not any(EMPTY_SPACE in row for row in grid.getGrid()):
                    if len(pruned)> 0:
                        draw_board(screen, grid, rows, cols, f"Tie Game! Pruned: {len(pruned)}")
                    else:
                        draw_board(screen, grid, rows, cols, "Tie Game!")
                    game_over = True
                else:
                    draw_board(screen, grid, rows, cols, "")
                turn += 1

        #exit loop if game has ended
        if game_over:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

#game loop variant that handles randomness for Expectiminimax
def stochastic_gui_game(player1_tuple, player2_tuple, rows, cols):
    player1_strategy, player1_label = player1_tuple
    player2_strategy, player2_label = player2_tuple

    #initlialize game environment and Pygame screen
    grid, game = setup_game(rows, cols)
    width = cols * SQUARESIZE
    height = (rows + 2) * SQUARESIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect-4 AI Game")

    turn = 1
    game_over = False

    #create an AdversarialSearch instance for managing vailid moves and randomness
    adversary = AdversarialSearch(rows,columns)

    #draw the initial empty game board
    draw_board(screen, grid, rows, cols, "Game Start!")

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #determine the current player based on the turn number
        current_player = PLAYER1_PIECE if turn % 2 == 1 else PLAYER2_PIECE
        strategy = player1_strategy if current_player == PLAYER1_PIECE else player2_strategy
        label = player1_label if current_player == PLAYER1_PIECE else player2_label
        player_name = f"Player {1 if current_player == PLAYER1_PIECE else 2}"
        player = game.players[0] if turn%2 == 1 else game.players[1]
        
        #human strategy block
        if strategy == human_strategy:
            #inject randomness every 4th turn based on the player
            if (current_player == PLAYER1_PIECE and turn%4 == 3) or (current_player == PLAYER2_PIECE and turn%4 == 0):
                #display random move message
                draw_board(screen, grid, rows, cols, f"{player_name}'s Random Move! ({label})")
                moves = adversary.getValidMoves(grid.getGrid())
                i = randint(0,len(moves)-1)
                grid.placePlayerPiece(moves[i],current_player)
                pygame.time.wait(2000)
                turn += 1

                #check if the move results in a win or tie
                if grid.checkWin(CONNECT_TARGET, current_player):
                        
                    draw_board(screen, grid, rows, cols, f"{player_name} wins!")
                    game_over = True
                elif not any(EMPTY_SPACE in row for row in grid.getGrid()):
                        
                    draw_board(screen, grid, rows, cols, "Tie Game!")
                    game_over = True

            else:
                #normal human turn - wait for mouse click input
                draw_board(screen, grid, rows, cols, f"{player_name}'s Turn (You)")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        posx = event.pos[0]
                        col = int(posx / SQUARESIZE)
                        if grid.getGrid()[0][col] == EMPTY_SPACE:
                            grid.placePlayerPiece(col, current_player)
                            if grid.checkWin(CONNECT_TARGET, current_player):
                                draw_board(screen, grid, rows, cols, f"{player_name} wins!")
                                
                                game_over = True
                            elif not any(EMPTY_SPACE in row for row in grid.getGrid()):
                            
                                draw_board(screen, grid, rows, cols, "Tie Game!")
                                game_over = True
                            else:
                                draw_board(screen, grid, rows, cols, "")
                            turn += 1
        #AI strategy block
        else:
            #Inject randomness for AI player every 4th turn
            if (current_player == PLAYER1_PIECE and turn%4 == 3) or (current_player == PLAYER2_PIECE and turn%4 == 0):
                draw_board(screen, grid, rows, cols, f"{player_name}'s Random Move! ({label})")
                moves = adversary.getValidMoves(grid.getGrid())
                i = randint(0,len(moves)-1)
                grid.placePlayerPiece(moves[i],current_player)
                pygame.time.wait(2000)
                turn += 1

                #check win or tie after each move
                if grid.checkWin(CONNECT_TARGET, current_player):
                        
                    draw_board(screen, grid, rows, cols, f"{player_name} wins!")
                    game_over = True
                elif not any(EMPTY_SPACE in row for row in grid.getGrid()):
                        
                    draw_board(screen, grid, rows, cols, "Tie Game!")
                    game_over = True


            
            else:
                #AI makes a strategic move
                draw_board(screen, grid, rows, cols, f"{player_name}'s Turn ({label})")
                pygame.time.wait(800)
                
                result = strategy(game, grid, player, turn)

                move = result if isinstance(result, int) else result[0]
                if move is not None and grid.getGrid()[0][move] == EMPTY_SPACE:
                    grid.placePlayerPiece(move, current_player)
                    #check if the AI's move results in a win or tie
                    if grid.checkWin(CONNECT_TARGET, current_player):
                        
                        draw_board(screen, grid, rows, cols, f"{player_name} wins!")
                        game_over = True
                    elif not any(EMPTY_SPACE in row for row in grid.getGrid()):
                        
                        draw_board(screen, grid, rows, cols, "Tie Game!")
                        game_over = True
                    else:
                        draw_board(screen, grid, rows, cols, "")
                    turn += 1

        #final game over screen loop (waits until user closes the window)
        if game_over:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

#entry point to launch GUI
if __name__ == "__main__":
    rows, columns = 6, 7  #set board size

    temp_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Connect-4 Settings")

    choice = show_menu(temp_screen, 600)

    if choice in {4, 5, 6, 7}:
        difficulty = select_difficulty(temp_screen, 600)
    else:
        difficulty = "hard"

    strategies = {
        1: ((human_strategy, "You"), (ai_strategy("minimax"), "Minimax")),
        2: ((human_strategy, "You"), (ai_strategy("alphabeta"), "Alpha-Beta")),
        3: ((human_strategy, "You"), (ai_strategy("expectiminimax"), "Expectiminimax")),
        4: ((human_strategy, "You"), (gemini_strategy(difficulty), f"Gemini-difficulty:{difficulty}")),
        5: ((gemini_strategy(difficulty), f"Gemini-difficulty:{difficulty}"), (ai_strategy("minimax"), "Minimax")),
        6: ((gemini_strategy(difficulty), f"Gemini-difficulty:{difficulty}"), (ai_strategy("alphabeta"), "Alpha-Beta")),
        7: ((gemini_strategy(difficulty), f"Gemini-difficulty:{difficulty}"), (ai_strategy("expectiminimax"), "Expectiminimax")),
        8: ((ai_strategy("minimax"), "Minimax"), (ai_strategy("minimax"), "Minimax")),
        9: ((ai_strategy("alphabeta"), "Alpha-Beta"), (ai_strategy("alphabeta"), "Alpha-Beta")), 
        10: ((ai_strategy("expectiminimax"), "Expectiminimax"), (ai_strategy("expectiminimax"), "Expectiminimax"))
    }

    player1, player2 = strategies[choice]
    
    if choice in {3,7,10}:
        stochastic_gui_game(player1, player2, rows, columns)
    else:
        gui_game(player1, player2, rows, columns)
