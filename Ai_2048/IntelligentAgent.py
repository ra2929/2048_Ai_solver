import random
import math
import time

from BaseAI import BaseAI


class IntelligentAgent(BaseAI):
    
    def getMove(self, grid):
        #gets all moves
        move_set = grid.getAvailableMoves()
        #return random.choice(move_set)[0] if move_set else None
    
        #time for each move
        self.time = time.clock()        
        max_depth = 2

        
        #best achievable payoff against best play. "Best move" DECSION(state) = getMove()
        move = self.maximize(grid, -math.inf, math.inf, max_depth)[0]
        for m in move_set:
            if m[1].map == move.map:
                return m[0]
    

        return None
        #choice is random is no move exists
        #return random.choice(move_set)[0]
        
    #min and max both need to have access to children
    def get_children(self, grid, max_val, tile_val=2):
        children = []
    
        #if child contains max
        if max_val:
            all_moves = grid.getAvailableMoves()
            for move in all_moves:
                next_move = move[1].clone()
                #print(next_move)
                #new move is either a "2" or a "4"
                children.append(next_move)
        else:
            all_moves = grid.getAvailableCells()
            for move in all_moves:		
                    next_move = grid.clone()
                    #calc next move
                    next_move.insertTile(move, tile_val)
                    #new move is either a "2" or a "4"
                    children.append(next_move)
        return (children)
    
    # Snake heuristic found at http://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    def snake_heuristic(self, grid):
        
        snake_grid = [[4**15,4**14,4**13,4**12],
                      [4**8,4**9,4**10,4**11],
                      [4**7,4**6,4**5,4**4],
                      [4**0, 4**1, 4**2,4**3]]

        score=0
        for x in range(3):
            for y in range(3):
                score+=grid.map[x][y]*snake_grid[x][y]
        return score
    
    #counts number of empty tiles
    def empty_tiles(self, grid):
        number_of_tiles = len(grid.getAvailableCells())
        return number_of_tiles

    # len(available cells)
    # eval(s) = heuristic(s) * weight			
    def evaluate(self, grid):
        weight = [1,2]
        return   self.empty_tiles(grid) * weight[0] + self.snake_heuristic(grid) 
    
    
    def chance(self,grid, alpha, beta, depth):
            
        return .9 * self.minimize(grid, alpha, beta, depth, 2)[1] + .1 * self.minimize(grid, alpha, beta, depth, 4)[1]
    
    def term_test(self, children):

        if len(children.getAvailableMoves()) == 0:
                return True
        return False

    #alpa = largest value for Max (current lower bound on MAX's outcome)
    #beta = lowest value for Min (current upper bound on MIN's outcome)
    #find the child with the highest utility value
    def maximize(self, grid, alpha, beta, depth):
        #if over time or there are no more moves
        if self.term_test(grid) or depth == 0 or (time.clock() - self.time) > 0.2:
            #if (time.clock() - self.time) > 0.2:
                #raise Exception(f'too much time of {(time.clock() - self.time)}')
            return (None, self.evaluate(grid))
        
        children = self.get_children(grid, max_val = True)
        
        max_child, max_utility = None, -math.inf
        
        for child in children:

            utility = self.chance(child, alpha, beta, depth)
            
            #alpha-beta pruning
            if utility > max_utility:
                max_child, max_utility = child,utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility
        
        #tuple of (State, Utility)
        return (max_child, max_utility)
            
    #find the child state will lowest utility value
    def minimize(self, grid, alpha, beta, depth, value):

        #if over time or there are no more moves
        if self.term_test(grid) or depth == 0 or (time.clock() - self.time) > 0.2:
            #if (time.clock() - self.time) > 0.2:
                #raise Exception(f'too much time of {(time.clock() - self.time)}')
            return (None, self.evaluate(grid))
        
        children = self.get_children(grid, max_val = False, tile_val = value)
        
        min_child, min_utility = None, math.inf

        for child in children:
            utility = self.maximize(child, alpha, beta, depth-1)[1]
            
            #alpha-beta pruning
            if utility < min_utility:
                min_child, min_utility = child,utility
            
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility
        #tuple of (State, Utility)
        return (min_child, min_utility)
    

