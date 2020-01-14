"""State for a Tic Tac Toe game.  Will contain 'X' and 'O' and -1 or -2"""
from copy import deepcopy

class GameState(object):
    def __init__(self, state):
        '''state is a list'''
        self.state = state
        self.winner = None #can also be 'X' or 'O'
        
    def __eq__(self, state):
        s1 = []
        s2 = []
        for val in state.state:
            if val is not 'X' and val is not 'O':
                s1.append(' ')
            else:
                s1.append(val)

        for val in self.state:
            if val is not 'X' and val is not 'O':
                s2.append(' ')
            else:
                s2.append(val)                
        return s1 == s2
    
    def __repr__(self):
        '''this is specifically for a tic tac toe state'''
        XO = []
        for val in self.state:
            if val is not 'X' and val is not 'O':
                XO.append(' ')
            else:
                XO.append(val)
        return "%s|%s|%s\n-+-+-\n%s|%s|%s\n-+-+-\n%s|%s|%s" % tuple(XO)

    def copy(self):
        '''Return a fresh copy of the state so we can modify it without effecting this one'''
        return deepcopy(self)
    
    def isEndState(self, filters):
        '''If this state is an end state, return True.  Otherwise False'''
        for f in filters:
            if self.filter(f):
                return True
        return False

    def setWinner(self, filters):
        '''Return the winner of this state: 'X' or 'O' or None if tie or no winners'''
        if self.winnerX(filters):
            self.winner = 'X'
        elif self.winnerO(filters):
            self.winner = 'O'
        
    def isWinner(self, symbol, f):
        '''Use the filters to check for a winner'''
        vals = [k for i, k in enumerate(self.state) if f[i] == 1]
        vals = list(set(vals))
        if len(vals) == 1:
            if vals[0] == symbol:
                return True
        return False

    def winnerX(self, filters):
        '''Check if "X" is the winner of this state'''
        for f in filters:
            if self.isWinner('X', f):
                return True
        return False

    def winnerO(self, filters):
        for f in filters:
            if self.isWinner('O', f):
                return True
        return False
    
    def filter(self, f):
        '''Pass in a filter and apply it to the state.  Return True or False.'''
        vals = [k for i, k in enumerate(self.state) if f[i] == 1]
        vals = list(set(vals))
        if len(vals) == 1:
            if vals[0] == 'X' or vals[0] == 'O':
                return True
        return False

    def setData(self, val, index):
        '''For human players, set a value by index, but don't overwrite if "X" or "O"'''
        if self.state[index] is not 'X' and self.state[index] is not 'O':
            self.state[index] = val
            return True
        return False

    
class StateTemplate(object):
    def __init__(self, state):
        self.state = state

    def __repr__(self):
        '''this is specifically for a tic tac toe state'''
        return "%s|%s|%s\n-+-+-\n%s|%s|%s\n-+-+-\n%s|%s|%s" % tuple(self.state)
