from environment import *
from copy import deepcopy
from random import randint



#Utility values
FOURS = 999999
THREES = 1000
TWOS = 10

class AdversarialSearch:
    
    def __init__(self, row, column):
        self.rows = row 
        self.columns = column

    #given a state, returns all column indexes that are valid
    def getValidMoves(self, currentGrid):
        validMoves = []
        for i in range(self.columns):
            if(currentGrid[0][i] == EMPTY_SPACE):
                validMoves.append(i)
        return validMoves

    #used in A/B pruning to get pruned nodes
    def getChildren(self,currentGrid, piece, moves):
        
        children = []

        for move in moves:
            tempGrid = deepcopy(currentGrid)
            for row in range(self.rows-1, -1, -1):
                    if tempGrid[row][move] == EMPTY_SPACE:
                        tempGrid[row][move] = piece
                        break 
            children.append(tempGrid)
        
        return children

    #places a piece on the currentgrid in [row][column]
    def makeMove(self, currentGrid, piece, column):

        tempGrid = deepcopy(currentGrid)
        for row in range(self.rows-1, -1, -1):
                if tempGrid[row][column] == EMPTY_SPACE:
                    tempGrid[row][column] = piece
                    break 
        return tempGrid

    #determines if the current grid is full (no moves) or if someone won
    def isTerminalState(self,currentGrid):

        if len(self.getValidMoves(currentGrid)) == 0 or self.checkWin(currentGrid,1) or self.checkWin(currentGrid,2):
            return True
        return False

    #checks for a winner
    def checkWin(self,currentGrid, piece):
            
            # check all directions for each cell (Horizontal, vertical, both diagonals)
            for row in range(self.rows):
                for col in range(self.columns):

                    #skip if current cell does not match player's piece
                    if currentGrid[row][col] != piece:
                        continue

                    # horiztonal - right
                    if col + CONNECT_TARGET <= self.columns:
                        if all(currentGrid[row][col + i] == piece for i in range(CONNECT_TARGET)):
                            return True
                        
                    # veritcal down
                    if row + CONNECT_TARGET <= self.rows:
                        if all(currentGrid[row + i][col] == piece for i in range(CONNECT_TARGET)):
                            return True
                        
                    # Diagonal down-right (negative slope) \
                    if row + CONNECT_TARGET <= self.rows and col + CONNECT_TARGET <= self.columns:
                        if all(currentGrid[row + i][col + i] == piece for i in range(CONNECT_TARGET)):
                            return True
                    
                    # diaganol up right (positive slope) /
                    if row - CONNECT_TARGET + 1 >= 0 and col + CONNECT_TARGET <= self.columns:
                        if all(currentGrid[row - i][col + i] == piece for i in range (CONNECT_TARGET)):
                            return True
            
            return False

    #utility function used in all algorithms
    #given a grid, it evaluate how favourable it is for 'piece' by determining the
    #number of twos, threes, and fours
    #subtracts the utility the other player has on current state
    #a line is defined as four pieces together and is parsed from every row,column,diagonal in the grid
    def utilityFunction(self,currentGrid, piece):
        utility = 0

        
        #total row score
        #goes through every row in the grid and determines how favourable it is
        for row in range(self.rows):
            for col in range(self.columns-3):
                line = []
                for i in range(4):
                    line.append(currentGrid[row][col+i]) 
                utility += self.evaluateLine(line,piece)

        #total column score
        for col in range(self.columns):
            for row in range(self.rows-3):
                line = []
                for i in range(4):
                    line.append(currentGrid[row+i][col]) 
                utility += self.evaluateLine(line,piece)

        #diagonal score (negative slope \)
        for row in range(self.rows-3):
            for col in range(self.columns-3):
                line = []
                for i in range(4):
                    line.append(currentGrid[row+i][col+i])
                utility += self.evaluateLine(line,piece)
        
        #diagonal score positive slope
        for row in range(3,self.rows):
            for col in range(self.columns-3):
                line = []
                for i in range(4):
                    line.append(currentGrid[row-i][col+i])
                utility += self.evaluateLine(line,piece)
            

        return utility

    #used by the utility function
    def evaluateLine(self,line,piece):

        score = 0

        if piece == 2: 
            opponent = 1
        else:
            opponent = 2


        if line.count(piece)==4:
            score+=FOURS
        
        elif line.count(piece) == 3 and line.count(EMPTY_SPACE)==1:
            score += THREES
        
        elif line.count(piece) == 2 and line.count(EMPTY_SPACE)==2:
            score += TWOS

        elif line.count(opponent)==4:
            score-=FOURS
        
        elif line.count(opponent) == 3 and line.count(EMPTY_SPACE)==1:
            score -= THREES
        
        elif line.count(opponent) == 2 and line.count(EMPTY_SPACE)==2:
            score -= TWOS

        return score


    def minimax(self,currentGrid, depth, isMaximizingPlayer,maxPiece,minPiece):

        #tracks number of visited nodes for performance checking
        visited = 1
        
        #full grid, winner, or search complete
        if (self.isTerminalState(currentGrid) or depth == 0):
            
            if(self.isTerminalState(currentGrid)):
                if self.checkWin(currentGrid,maxPiece):
                    return 999999999, None, visited
                elif self.checkWin(currentGrid,minPiece):
                    return -999999999, None, visited
                else:
                    return 0,None, visited
            else:
                #get utility wrt AI
                return self.utilityFunction(currentGrid,maxPiece), None, visited


        if (isMaximizingPlayer):

            bestValue = -9999999999 #temp neg infinity
            
            # gives all columns that you can place a move
            for move in self.getValidMoves(currentGrid):

                # assuming AI only plays as player 2
                child = self.makeMove(currentGrid, maxPiece, move)

                value , x, nodesVisited = self.minimax(child,depth-1,False,maxPiece,minPiece)

                visited += nodesVisited

                if value > bestValue:
                    bestMove = move
                    bestValue = value

            return bestValue, bestMove, visited 
        
        else:
            bestValue = 9999999999 #temp pos infinity
            
            # gives all columns that you can place a move
            for move in self.getValidMoves(currentGrid):

                # assuming non AI only plays as player 1
                child = self.makeMove(currentGrid, minPiece, move)

                value, x, nodesVisited = self.minimax(child,depth-1,True,maxPiece,minPiece)
                
                visited += nodesVisited

                if value < bestValue:
                    bestMove = move
                    bestValue = value

            return bestValue, bestMove, visited

    #used in A/B pruning to restore branches
    def generateBranch(self, prunedGrid, depthPruned, wasMaximizer,maxPiece,minPiece, restoredBranch):

        if depthPruned <= 0 or self.checkWin(prunedGrid,1) or self.checkWin(prunedGrid,2):
            restoredBranch.append(prunedGrid)
            return 
        
        if (wasMaximizer):

            bestValue = -9999999999 #temp neg infinity
            
            # gives all columns that you can place a move
            for move in self.getValidMoves(prunedGrid):

                # assuming AI only plays as player 2
                child = self.makeMove(prunedGrid, maxPiece, move)

                value, _,_ = self.minimax(child,depthPruned-1,False,maxPiece,minPiece)

                restoredBranch.append(child)

                if value > bestValue:
                    bestValue = value

            return bestValue
        
        else:
            bestValue = 9999999999 #temp pos infinity
            
            # gives all columns that you can place a move
            for move in self.getValidMoves(prunedGrid):

                # assuming non AI only plays as player 1
                child = self.makeMove(prunedGrid, minPiece, move)

                value, _, _ = self.minimax(child,depthPruned-1,True,maxPiece,minPiece)

                if value < bestValue:
                    bestValue = value
                restoredBranch.append(child)

            return bestValue


    # the pruned array will be an array where each value is another array in form [pruned child, depth, player]
    # will use the generate tree to get the branch that was pruned off from using AB pruning 
    def alphaBetaPruning(self, currentGrid, depth, alpha, beta, isMaximizingPlayer, maxPiece,minPiece, pruned):
        
        visited = 1

        if (self.isTerminalState(currentGrid) or depth == 0):
            #AI won
            if(self.isTerminalState(currentGrid)):
                if self.checkWin(currentGrid,maxPiece):
                    return 999999999, None, visited
                elif self.checkWin(currentGrid,minPiece):
                    return -999999999, None, visited
                else:
                    return 0,None, visited
            else:
                #get utility wrt AI
                return self.utilityFunction(currentGrid,maxPiece), None, visited

        if (isMaximizingPlayer):

            bestValue = -9999999999 #temp neg infinity
            
            # gives all columns that you can place a move
            moves = self.getValidMoves(currentGrid)
            for i in range(len(moves)):

                # assuming AI only plays as player 2
                child = self.makeMove(currentGrid, maxPiece, moves[i])

                value,_, childNodes = self.alphaBetaPruning(child,depth-1,alpha,beta,False,maxPiece,minPiece, pruned)
                visited += childNodes

                if value > bestValue:
                    bestMove = moves[i]
                    bestValue = value
                
                alpha = max(alpha,value)

                #prune rest of children
                if alpha >= beta:
                    #used for visualizing later
                    for child in self.getChildren(currentGrid, maxPiece, moves[i+1:]):

                        #assuming it went to child, it would be the minimizing turn
                        pruned.append([child, depth-1, False,maxPiece,minPiece])

                    break

            return bestValue, bestMove, visited
        
        else:
            bestValue = 9999999999 #temp pos infinity
            
            # gives all columns that you can place a move
            moves = self.getValidMoves(currentGrid)
            for i in range(len(moves)):

                # assuming non AI only plays as player 1
                child = self.makeMove(currentGrid, minPiece, moves[i])

                value,_, childNodes = self.alphaBetaPruning(child,depth-1,alpha,beta,True,maxPiece,minPiece,pruned)
                visited+= childNodes

                if value < bestValue:
                    bestMove = moves[i]
                    bestValue = value

                beta = min(beta, value)

                if beta <= alpha:
                    #used for visualizing later
                    for child in self.getChildren(currentGrid, minPiece, moves[i+1:]):

                        #assuming it went to child, it would be maximizing turn
                        pruned.append([child, depth-1, True,maxPiece,minPiece])

                    break

            return bestValue, bestMove, visited


    def isChanceNode(self, turnNumber):
        #every other turn for Player 1 and 2 will be a randomly selected move
        return turnNumber%4==0 or turnNumber%4 ==3
        

    def expectiminiMax(self,currentGrid, depth, isMaximizingPlayer,turnNumber, maxPiece, minPiece):

        visited = 1
        
        if depth <= 0 or self.isTerminalState(currentGrid):
            #AI won
            if(self.isTerminalState(currentGrid)):
                if self.checkWin(currentGrid,maxPiece):
                    return 999999999, None, visited
                elif self.checkWin(currentGrid, minPiece):
                    return -999999999, None, visited
                else:
                    return 0,None, visited
            else:
                #get utility wrt AI
                return self.utilityFunction(currentGrid,maxPiece), None, visited
        
        if self.isChanceNode(turnNumber):

            #isMaximizing check is only to differentiate the next call

            if isMaximizingPlayer:
                expectedValue = 0
                moves = self.getValidMoves(currentGrid)
                #every move has equal probability of being selected
                prob = 1/len(moves)

                for i in range(len(moves)):
                    child = self.makeMove(currentGrid,maxPiece, moves[i])
                    value,_, childVisits = self.expectiminiMax(child,depth-1,False,turnNumber+1,maxPiece,minPiece)
                    expectedValue += value*prob
                    visited += childVisits
                
                return expectedValue, None, visited

            else:
                expectedValue = 0
                moves = self.getValidMoves(currentGrid)
                prob = 1/len(moves)
                for i in range(len(moves)):
                    child = self.makeMove(currentGrid,minPiece, moves[i])
                    value,_, childVisits = self.expectiminiMax(child,depth-1,True,turnNumber+1,maxPiece,minPiece)
                    expectedValue += value*prob
                    visited += childVisits
                
                return expectedValue, None, visited
            

        #same as minimax
        elif isMaximizingPlayer:

            bestValue = -9999999999
            moves = self.getValidMoves(currentGrid)

            for i in range(len(moves)):
                

                child = self.makeMove(currentGrid, maxPiece, moves[i])

                value,_, childVisits = self.expectiminiMax(child,depth-1,False,turnNumber+1,maxPiece,minPiece)
                visited += childVisits

                if value > bestValue:
                    bestMove = moves[i]
                    bestValue = value
                

            return bestValue, bestMove, visited

        else:
            bestValue = 9999999999
            moves = self.getValidMoves(currentGrid)
            

            for i in range(len(moves)):

                child = self.makeMove(currentGrid, minPiece, moves[i])

                value,_, childVisits = self.expectiminiMax(child,depth-1,True,turnNumber+1,maxPiece,minPiece)
                visited += childVisits

                if value < bestValue:
                    bestMove = moves[i]
                    bestValue = value
                

            return bestValue, bestMove, visited
