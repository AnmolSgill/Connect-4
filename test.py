from environment import *
from minimax import *
from main import *

#
#grid = Connect4Board(6, 7)
#grid.getGrid()[3][4] = 1
#grid.getGrid()[3][5] = 2
#grid.getGrid()[2][1] = 1

#pruned = []
#_,i = minimax(grid.getGrid(),6,True)
#_,x = alphaBetaPruning(grid.getGrid(),6,-999999999,999999999,True,pruned)
#print(i)
#print(x)

#print(len(pruned))
#

#grid = Connect4Board(6, 7)
#game = Game(grid)

def runMiniMax():

    rows = game.grid.getRow()
    cols = game.grid.getColumns()

    miniMaxGame = AdversarialSearch(rows, cols)

    
    winner = False
    visits = 0
    
    while not winner:
        for p in game.players:
            if p.getPiece() == 1:

                placePiece = game.simulatePlayerMove(p)
                if game.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    print(p.getName())
                    game.printConnect4Board()
                    winner = True
            else:
                _,i,visited = miniMaxGame.minimax(grid.getGrid(),6,True)
                visits += visited 

                placePiece = game.grid.placePlayerPiece(i, p.getPiece())
                if game.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    print(p.getName())
                    game.printConnect4Board()
                    winner = True
    
    return visits


def runAlphaBeta():

    rows = game.grid.getRow()
    cols = game.grid.getColumns()

    alphaBetaGame = AdversarialSearch(rows, cols)

    pruned = []
    winner = False
    visits = 0

    while not winner:
        for p in game.players:
            if p.getPiece() == 1:

                placePiece = game.simulatePlayerMove(p)
                if game.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    print(p.getName())
                    game.printConnect4Board()
                    winner = True
            else:
                _,i, visited = alphaBetaGame.alphaBetaPruning(grid.getGrid(),6,-999999999,999999999,True,pruned)
                visits += visited

                placePiece = game.grid.placePlayerPiece(i, p.getPiece())
                if game.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    print(p.getName())
                    game.printConnect4Board()
                    winner = True
    
    restored = []
    for prune in pruned:
        branch = []
        alphaBetaGame.generateBranch(prune[0],prune[1],prune[2],branch)
        restored.append(branch)

    return restored,visits

def runExpectiminiMax():
    winner = False
    turns = 1

    rows = game.grid.getRow()
    cols = game.grid.getColumns()

    expectiGame = AdversarialSearch(rows, cols)
    visits = 0

    while not winner:
        
        for p in game.players:
            


            if p.getPiece() == 1:

                if turns % 4 == 3:
                    print()
                    print("Random Move!")
                    print()
                    moves = expectiGame.getValidMoves(grid.getGrid())
                    i = randint(0,len(moves)-1)
                    game.grid.placePlayerPiece(moves[i],p.getPiece())
                    game.printConnect4Board()
                    #print(p.getPiece() + "was placed in column " + (moves[i]+1))
                    print()
                    print(f"{p.getPiece()} was placed in column {moves[i]+1}")
                    print()
                    

                else:
                    placePiece = game.simulatePlayerMove(p)
                if game.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    print(p.getName())
                    game.printConnect4Board()
                    winner = True
                
                turns +=1
            else:

                if turns %4 == 0:
                    print()
                    print("Random Move!")
                    print()
                    moves = expectiGame.getValidMoves(grid.getGrid())
                    i = randint(0,len(moves)-1)
                    game.grid.placePlayerPiece(moves[i],p.getPiece())
                    game.printConnect4Board()
                    #print(p.getPiece() + "was placed in column " + (moves[i]+1))
                    print()
                    print(f"{p.getPiece()} was placed in column {moves[i]+1}")
                    print()
                    

                else:
                    _,i,visited = expectiGame.expectiminiMax(grid.getGrid(),6,True,turns)
                    visits += visited 

                    placePiece = game.grid.placePlayerPiece(i, p.getPiece())
                if game.grid.checkWin(CONNECT_TARGET, p.getPiece()):
                    print(p.getName())
                    game.printConnect4Board()
                    winner = True

                turns += 1
    return visits 



#before running tests have to comment out game.gameplay() in main
#visits = runExpectiminiMax()

#visits = runMiniMax()

#this will take a long time but it gets every branch that was pruned off
#
"""
a,visits = runAlphaBeta()
for grid in a:
    for row in grid:
        for col in row:
            print(col)
    print()
"""
