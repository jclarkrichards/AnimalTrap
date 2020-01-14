"""Handles any method that deals with setting up and playing a tic tac toe game"""
from tree import Tree
from state import GameState, StateTemplate
from copy import deepcopy

def filters():
    '''Filters to use to check for end states'''
    return [[1,1,1,0,0,0,0,0,0],
            [0,0,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,1,1,1],
            [1,0,0,1,0,0,1,0,0],
            [0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,1,0,0,1],
            [1,0,0,0,1,0,0,0,1],
            [0,0,1,0,1,0,1,0,0]]


class TicTacToe(object):
    def __init__(self):
        self.tree = None
        self.xplayer = False #True if human player
        self.oplayer = False #True if human player
        self.gameover = False
        self.xturn = True #False if oturn
        self.template = StateTemplate([0,1,2,3,4,5,6,7,8])
        self.startState = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        
    def setupTree(self):
        '''Set up the full tree which shows all of the game states'''
        self.tree = Tree()
        self.tree.root.data = GameState(self.startState)
        node = self.tree.root
        while node is not None:
            if -1 in node.data.state:
                nodestate = deepcopy(node.data.state)
                index = nodestate.index(-1)
                node.data.state[index] = -2
                node = self.tree.addNode(node)
                #node = self.tree.findNode(nodeid)
                if len([k for k in nodestate if k == -1 or k == -2]) % 2:
                #if len(node.id) % 2 == 0:
                    nodestate[index] = 'X'
                else:
                    nodestate[index] = 'O'
                    
                for i in range(len(nodestate)):
                    if nodestate[i] == -2:
                        nodestate[i] = -1
                node.data = GameState(nodestate)
                #node.depth = len(node.id)-1 #depth is 0-based
            else:
                node = node.parent

        self.tree.prune(self.tree.root, filters()) #prune the tree with the filters
        

    def checkEndGame(self):
        '''Return true if the current node has no children'''
        if len(self.tree.root.children) == 0:
            return True
        return False

    def humanFirstTurn(self):
        return int(raw_input("Enter an 'X' at location: (0-8) "))
        
    def humanTurn(self, symbol):
        '''Gets called when it is a humans turn.  symbol is either "X" or "O"'''
        i = int(raw_input("Enter an '"+symbol+"' at location: (0-8) "))
        data = self.tree.root.data.copy()
        if not data.setData(symbol, i):
            print("Cannot place '"+symbol+"' there.  Try again")
            self.humanTurn(symbol)
        else:
            node = self.tree.find(data)
            self.tree.setRoot(node.id)

    #def aiTurn(self, symbol, index):
    #    '''The ai at this point has chosen the best path as given by the index'''
    #    data = self.tree.root.data.copy() #get a copy of root GameState
    #    #data.setData(symbol, index)
    #    node = self.tree.find(data)
    #    self.tree.setRoot(node.id)

    def makeMoveAI(self, index):
        node = self.tree.root.children[index]
        self.tree.setRoot(node.id)

    #def checkChildScores(self):
    #    '''What are the scores for the children of root?'''
    #    #d = {'X':0, 'O':0, 'BOTH':0}
    #    print("Checking child scores...")
    #    self.tree.scoreTest(filters())
        
