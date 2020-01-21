"""Handles any method that deals with setting up and playing a tic tac toe game"""
from tree import Tree
from state import GameState, StateTemplate
from copy import deepcopy
from constants import *
#from utils import *
import utils
from state import *
from random import randint

"""Maybe the first few turns the computer takes are random.  If the computer makes the first move, it does not matter where that move is really.  Maybe after 4 moves we do the monte carlo.  When we are down to just a fews moves left we can start making trees."""

class AnimalTrap(object):
    def __init__(self):
        self.tree = None
        self.player = 1 #game start with player 1
        self.player1Human = False
        self.player2Human = False
        self.gameover = False
        self.template = StateTemplate()
        #self.startState = [1,2,0,2,0,0,-2,0,1,1,2,1,2,1,1,2]
        #self.startState = [1,0,0,2,0,0,0,0,0,1,1,1,-2,0,2,2]
        #startState = [-1,-1,0,-2,-1,0,2,0,1,0,0,-2,0,0,0,0]
        startState = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.state = GameState(startState)
        
    def setPlayers(self):
        '''Set which players are human'''
        human = raw_input("Is Player 1 human? (y/n) ")
        if human == 'y': self.player1Human = True
        human = raw_input("Is Player 2 human? (y/n) ")
        if human == 'y': self.player2Human = True

    def getOtherPlayer(self):
        if self.player == 1: return 2
        return 1
    
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
        #print("montecarlo")
        #print(state)
        while not state.endState():
            state = self.getRandomState(state)
            #print("Player " + str(self.player))
            #print(">>>>>>>>>>>>>>>>")
            #print(state)
            self.getNextPlayer()
            turns += 1
            if firstMove:
                firstMoveState = deepcopy(state)
            firstMove = False
        winners = state.getWinners()
        #print(".............")
        #print(firstMoveState)
        return firstMoveState, turns, winners

    def setNextStateAuto(self):
        '''Perform monte carlo a bunch of times to try and find the next best state.  We can add to the results if we need more data.'''
        results = []
        print("Starting results")
        print(results)
        print("START STATE")
        print(self.state)
        self.setPlayer()
        print("Player " + str(self.player))
        template = {"turns":0, "state":None, "winners":[]}
        if not self.state.endState():
            for i in range(1000):
                #print("---------------------------------------")
                self.setPlayer()
                state = self.state.copy()
                #print("STATE")
                #print(state)
                #print("---------------")
                firstState, turns, winners = self.montecarlo(state)
                #print("next possible state")
                #print(firstState)
                #print("++++++++++++++++++++++++++++++++++++++++")
                temp = deepcopy(template)
                temp["turns"] = turns
                temp["state"] = deepcopy(firstState)
                temp["winners"] = winners
                results.append(temp)

        #print("RESULTS")
        
        #print(results)
        #analyze the data to determine the next best state
        #for i in range(len(results)):
        #    print(results[i])
        #    print("")
        #return results
        self.analyzeData(results)
        #print("THIS IS THE NEW STATE")
        #print(results[0]["state"].data)
        #print("+++++++++++++++++++++")
        #self.state = GameState(results[0]["state"].data)
        
    def analyzeData(self, results):
        '''Determine the next best move from the data.  Can get more data by calling getNextState again'''
        #print("RAW RESULTS")
        #print(results)
        #print("")
        #print("")
        self.setPlayer()
        #print("ANALYZE Best move for Player " + str(self.player))
        fullDict = {}
        stateDict = {}
        num = 0
        states = [k['state'] for k in results]
        for i in range(len(results)):
            if results[i]['state'] not in stateDict.values():
                stateDict[num] = results[i]['state']
                fullDict[num] = {}
                if results[i]['winners'][1] > 0 or results[i]['winners'][2] > 0:
                    fullDict[num][results[i]['turns']] = {1:0, 2:0}
                    fullDict[num][results[i]['turns']][1] += results[i]['winners'][1]
                    fullDict[num][results[i]['turns']][2] += results[i]['winners'][2]
                num += 1
            else:
                n = -1
                for key in stateDict.keys():
                    if stateDict[key] == results[i]['state']:
                        n = key
                        break

                if results[i]['turns'] not in fullDict[n]:
                    if results[i]['winners'][1] > 0 or results[i]['winners'][2] > 0:
                        fullDict[n][results[i]['turns']] = {1:0, 2:0}
                        fullDict[n][results[i]['turns']][1] += results[i]['winners'][1]
                        fullDict[n][results[i]['turns']][2] += results[i]['winners'][2]
                else:
                    fullDict[n][results[i]['turns']][1] += results[i]['winners'][1]
                    fullDict[n][results[i]['turns']][2] += results[i]['winners'][2]
                

        #print("DICTIONARIES")
        #print(stateDict)
        #print("")
        #print("")
        allturnsSorted = []
        for key in fullDict.keys():
            #print(str(key) + " : " + str(fullDict[key]))
            #print("")
            allturnsSorted += fullDict[key].keys()
            
        #print("All turns unsorted: " + str(allturnsSorted))
        allturnsSorted = list(set(allturnsSorted))
        allturnsSorted.sort()
        #print("All turn sorted: " + str(allturnsSorted))
        #example:  {index: {turns:{p1:#wins, p2:#wins}}}
        #{0: { 9 : {1:3, 2:5}, 4: {1:2, 2:0}}, 1: {5:{1:0, 2:2}}}
        #for i in range(len(results)):
        #    pass

        #Start with the smallest turns, in any of those does the player win without the other player winning?
        tempStateIndices = []
        turn = allturnsSorted.pop(0)
        other = self.getOtherPlayer()
        for key in fullDict.keys():
            if turn in fullDict[key].keys():
                #print(key)
                #print(fullDict[key])
                if fullDict[key][turn][self.player] > fullDict[key][turn][other]:
                    print("Getting a jump on the win")
                    tempStateIndices.append((key, turn))

        if len(tempStateIndices) == 0:
            #print("Need to either get more data or check the next value in allturnsSorted")
            while len(tempStateIndices) == 0 and len(allturnsSorted) > 0:
                #print("status check: " + str(len(tempStateIndices)))
                turn = allturnsSorted.pop(-1)
                #print("Checking turn " + str(turn))
                #print(allturnsSorted)
                for key in fullDict.keys():
                    if turn in fullDict[key].keys():
                        #print("found one at " + str(key)+" : " + "1:"+str(fullDict[key][turn][self.player]) + ", 2:"+str(fullDict[key][turn][other]))
                        if fullDict[key][turn][self.player] < fullDict[key][turn][other]:
                            print("Just making sure you don't win")
                            tempStateIndices.append((key, turn))
        #else:
        #    print("Found some, good!")

        #print("DID WE DO GOOD????")
        #print("What are the chances that we still have an empty array here?")
        
        print(tempStateIndices)
        #print(self.state)
        if len(tempStateIndices) > 0:
            #print("Choosing state " + str(tempStateIndices[0][0]))
            #For now just choose the first entry so that we can play the game
            #We want to be able to choose the best entry though
            #print("OLD STATE")
            #print(self.state)
            #print("CHOOSING STATE")
            #print(stateDict[tempStateIndices[0][0]])
            #self.state = GameState(stateDict[tempStateIndices[0][0]].data)
            self.state = stateDict[tempStateIndices[0][0]]
            #print("CURRENT STATE")
            #print(self.state)
        else:
            print("UHHHHHHHHHH!  Now what???")

    def checkEndGame(self):
        '''Sets gameover variable to True if our current state is an end state'''
        if self.state.endState(): self.gameover = True

    def nextTurn(self):
        raw_input("Hit any key to continue... ")
        
    def getHumanChoice(self):
        '''Return a tuple that describes a move (flip index (from), flip index (to), place index, 1 or -1).  Need to add checks to make sure not making illegal moves.'''
        flipfrom = None
        flipto = None
        if len([k for k in self.state.data if k == 0]) < 16:
            valid = False
            while not valid:
                flipfrom = int(raw_input("Flip from index: "))
                if self.state.data[flipfrom] == 0:
                    #if abs(self.state.data[flipfrom]) == self.player:
                    print("NOT VALID!  Choose again!")
                else:
                    if abs(self.state.data[flipfrom]) != self.player:
                        valid = True
                    else:
                        print("Can't flip own piece!  Try again!")
                
            valid = False
            while not valid:
                adjacents = utils.getAdjacentIndices(self.state, flipfrom)
                print("Valid choices: " + str(adjacents))
                flipto = int(raw_input("Flip to index: "))
                if flipto not in adjacents:
                    print("NOT VALID!  Choose again!")
                else:
                    valid = True
                
        valid = False
        while not valid:
            place = int(raw_input("Place own piece on index: "))
            if self.state.data[place] != 0:
                if place != flipfrom:
                    print("NOT VALID!  Choose again!")
                else:
                    valid = True
            else:
                if flipto is not None:
                    if place != flipto:
                        valid = True
                    else:
                        print("NOT VALID!  Choose again!")
                else:
                    valid = True
                
        side = raw_input("Negative or positive? (n/p) ")
        if side == 'n': return (flipfrom, flipto, place, -1)
        return (flipfrom, flipto, place, 1)

    def setState(self, values):
        '''Set the current state based on a tuple of 4 values'''
        flipfrom, flipto, place, side = values
        if flipfrom is not None and flipto is not None:
            othervalue = self.state.data[flipfrom]
            self.state.data[flipfrom] = 0
            self.state.data[flipto] = othervalue * -1
        self.state.data[place] = self.player * side
        #print(self.state)

    

        
        
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

        
