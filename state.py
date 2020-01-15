from copy import deepcopy
from constants import *
import utils

class GameState(object):
    def __init__(self, data):
        '''state is a list'''
        #state=[0,0,0,0,-2,0,0,0,0,-1,0,0,1,0,2,0]
        self.data = data
        self.winner = None

    """
    def __eq__(self, state):
        '''Does state equal this state?'''
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
    """
    def __repr__(self):
        '''How we want to print the state to the screen'''
        S = []
        for val in self.data:
            if val == 0:
                S.append(' ')
            else:
                S.append(val)
        return "%s|%s|%s|%s\n-+-+-+-\n%s|%s|%s|%s\n-+-+-+-\n%s|%s|%s|%s\n-+-+-+-\n%s|%s|%s|%s\n" % tuple(S)

    def copy(self):
        '''Return a fresh copy of the state so we can modify it without effecting this one'''
        return deepcopy(self)

    def getFlipState(self, iplace, iflip):
        '''Given a state, flip piece at index i to index iflip'''
        newstate = self.copy()
        newstate.data[iflip] = newstate.data[iplace] * -1
        newstate.data[iplace] = 0
        return newstate #type GameState

    def endState(self):
        '''Return True if this state is an end state'''
        #print("CHECK END STATE")                                                            
        filterDict = self.matchFilters()
        if len(filterDict) != 0:
            for key in filterDict.keys():
                for f in filterDict[key]:
                    indices = utils.getIndices(f, 1)
                    F = utils.getValidFlipLocations(self.data, indices)
                    is_end_state = True
                    for k in F.keys():
                        if len(F[k]) > 0:
                            is_end_state = False
                    if is_end_state:
                        return True
        else:
            indices = utils.getIndices(self.data, 0)
            if len(indices) == 0:
                return True
        return False

    def matchFilters(self):
        '''Check the state against all of the filters.  Return True if there is a match on any of the filters.'''
        #print(state)                                                                        
        correctFilters = {}
        for f in filters:
            #print(f)                                                                         
            result = []
            #print(len(f))                                                                    
            for i in range(len(f)):
                if f[i] == 1:
                    #print(str(f[i]) + ", " + str(state[i]))                                    
                    result.append(self.data[i])
            #print("RESULT = " + str(result))                                                 
            result = list(set(result))
            #print("RESULT = " + str(result))                                                 
            if len(result) == 1:
                if result[0] != 0:
                    if result[0] not in correctFilters:
                        correctFilters[result[0]] = [f]
                    else:
                        correctFilters[result[0]].append(f)

        return correctFilters

    def getWinners(self):
        '''Assuming the state is an end state, get a list of winners.  Can have the same winner multiple times if the winner has multiple winning lines.'''
        filterDict = self.matchFilters()
        if len(filterDict) != 0:
            winners = {}
            for key in filterDict.keys():
                if abs(key) not in winners:
                    winners[abs(key)] = 1
                else:
                    winners[abs(key)] += 1
            return winners
        return None







    """
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
    """
    
    
class StateTemplate(object):
    def __init__(self):
        self.state = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    def __repr__(self):
        '''this is specifically for a tic tac toe state'''
        return "%s|%s|%s|%s\n-+-+-+-\n%s|%s|%s|%s\n-+-+-+-\n%s|%s|%s|%s\n-+-+-+-\n%s|%s|%s|%s\n" % tuple(self.state)
