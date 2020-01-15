"""Handles any method that deals with setting up and playing a tic tac toe game"""
from tree import Tree
from state import GameState, StateTemplate
from copy import deepcopy
from constants import *
#from utils import *
import utils
from state import *
from random import randint

class AnimalTrap(object):
    def __init__(self):
        self.tree = None
        self.player = 1 #game start with player 1
        self.player1Human = False
        self.player2Human = False
        self.gameover = False
        self.template = StateTemplate()
        self.startState = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.state = GameState(self.startState)
        
    def setPlayers(self):
        '''Set which players are human'''
        human = raw_input("Is Player 1 human? (y/n) ")
        if human == 'y': self.player1Human = True
        human = raw_input("Is Player 2 human? (y/n) ")
        if human == 'y': self.player2Human = True

    def getNextPlayer(self):
        '''Players switch back and forth'''
        if self.player == 1: self.player = 2
        else: self.player = 1

    def setPlayer(self):
        '''Set the player based on how many blank spaces are left:  even: player1'''
        numblank = len([k for k in self.state.data if k == 0])
        if numblank % 2: #odd
            self.player = 2
        else: self.player = 1

    def indicesOfOtherPlayer(self, state):
        '''Return a list of indices where the other players pieces are'''
        if self.player == 1:
            indices = utils.getIndices(state.data, PLAYERVALUES[2])
        else:
            indices = utils.getIndices(state.data, PLAYERVALUES[1])
        return indices

    def getRandomState(self, state):
        '''Given any state return a random next state'''
        indicesOP = self.indicesOfOtherPlayer(state)
        flipIndices = utils.getValidFlipLocations(state.data, indicesOP)

        if len(flipIndices) > 0:
            #print(flipIndices)                                                               
            keys = flipIndices.keys()
            #print(keys)                                                                      
            ikey = randint(0, len(keys)-1)
            #print(ikey)                                                                      
            #print(flipIndices[keys[ikey]])                                                   
            iflip = randint(0, len(flipIndices[keys[ikey]])-1)
            flipindex = flipIndices[keys[ikey]][iflip]
            #print("flip "+str(keys[ikey]) + " to " + str(flipindex))
            flipstate = state.getFlipState(keys[ikey], flipindex)
            #print(flipstate)                                                                 
            #print("==============================")                                          
            indices = utils.getIndices(flipstate.data, 0)
            #print("Zero indices: " + str(indices))                                           
            index = randint(0, len(indices)-1)
            iplayer = randint(0,1)
            p = PLAYERVALUES[self.player][iplayer]
            newstate = flipstate.copy()
            newstate.data[indices[index]] = p
        else:
            indices = utils.getIndices(state.data, 0)
            index = randint(0, len(indices)-1)
            iplayer = randint(0,1)
            p = PLAYERVALUES[self.player][iplayer]
            newstate = state.copy()
            newstate.data[index] = p
            
        return newstate
    
    def montecarlo(self, state):
        '''Make random decisions all the way to an end state'''
        turns = 0
        firstMove = True
        firstMoveState = []
        
        while not state.endState():
            state = self.getRandomState(state)
            print("Player " + str(self.player))
            print(state)
            self.getNextPlayer()
            turns += 1
            if firstMove:
                firstMoveState = state
            firstMove = False
        winners = state.getWinners()
        return firstMoveState, turns, winners

    def getNextState(self, startState, results=[]):
        '''Perform monte carlo a bunch of times to try and find the next best state.  We can add to the results if we need more data.'''
        #results = []
        template = {"turns":0, "state":None, "winners":[]}
        if not self.state.endState():
            for i in range(10):
                self.setPlayer()
                state = startState.copy()
                firstState, turns, winners = self.montecarlo(state)
                temp = deepcopy(template)
                temp["turns"] = turns
                temp["state"] = firstState
                temp["winners"] = winners
                results.append(temp)

        #analyze the data to determine the next best state
        for i in range(len(results)):
            print(results[i])
            print("")
            
        self.analyzeData(results)
        
        #print(allTurns)
        #print("")
        #print(allWinners)
        #print("")
        #print(allFirstStates)
        
    def analyzeData(self, results):
        '''Determine the next best move from the data.  Can get more data by calling getNextState again'''
        pass
        
    """
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

    def makeMoveAI(self, index):
        node = self.tree.root.children[index]
        self.tree.setRoot(node.id)
    """

        
