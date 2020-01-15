from tree import Tree
from copy import deepcopy
from random import randint

NUMROWS = 4
NUMCOLS = 4

filters = [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
           [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
           [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0],
           [0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0],
           [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
           [0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
           [0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0],
           [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
           [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
           [0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0],
           [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
           [0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0],
           [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0],
           [0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0]]

def getIndices(L, val):
   '''Given a list L return a list of indices where we see the value val.
   val can be a single value or a list of values'''
   indices = []
   if type(val) is list:
      for i in range(len(L)):
         if L[i] in val:
            indices.append(i)
   else:
      for i in range(len(L)):
         if L[i] == val:
            indices.append(i)
   return indices

def indicesOfOtherPlayer(L, player):
   '''Return a list of indices where the other players pieces are'''
   if player == 1:
      indices = getIndices(L, [2, -2])
   else:
      indices = getIndices(L, [1, -1])
   return indices

def getRow(index):
   '''Given an index, return the row number on the board'''
   return index / NUMROWS

def getColumn(index):
   return index % NUMCOLS

def getIndexFromRowCol(row, column):
   '''Given a row and column value, return the index on the board'''
   #print("r="+str(row) + ", c="+str(column))
   if row >= 0 and row < NUMROWS:
      if column >= 0 and column < NUMCOLS:
         return row*NUMCOLS + column
   return None

def getAdjacentIndices(S, val):
   '''Return a list of adjacent indices to val in S'''
   row = getRow(val)
   column = getColumn(val)
   #print("ROW="+str(row) + ", COL="+str(column))
   indices = []
   indices.append(getIndexFromRowCol(row+1, column))
   indices.append(getIndexFromRowCol(row-1, column))
   indices.append(getIndexFromRowCol(row, column+1))
   indices.append(getIndexFromRowCol(row, column-1))
   #print("I: " + str(indices))
   return [k for k in indices if k is not None]
   

def getValidFlipLocations(S, L):
   '''Given the state S and a list of indices L, return a dictionary where
   each entry in L is a key and the values are a list of adjacent indices'''
   D = {}
   #print(S)
   #print("L: " + str(L))
   for val in L:
      adjacents = getAdjacentIndices(S, val)
      #print("Adjacents: " + str(adjacents))
      junk = [k for k in adjacents if S[k] == 0]
      if len(junk) > 0:
         D[val] = junk
   return D

def getFlipState(state, i, iflip):
   '''Given a state, flip piece at index i to index iflip'''
   newstate = deepcopy(state)
   newstate[iflip] = newstate[i] * -1
   newstate[i] = 0
   return newstate

def getNextPlayer(player):
   if player == 1: return 2
   else: return 1
   
def constructTree(rootPlayer, maxdepth=-1):
   def recurse(node, player):
      nextPlayer = getNextPlayer(player)
      state = deepcopy(node.data)
      #find all of the other players values
      indicesOP = indicesOfOtherPlayer(state, player)
      #with the location of all of the other players pieces, get an
      #adjacency list (dictionary) of the open adjacent locations
      #print("")
      flipIndices = getValidFlipLocations(state, indicesOP)
      if len(flipIndices) > 0:
         for key in flipIndices.keys():
            for iflip in flipIndices[key]:
               flipstate = getFlipState(state, key, iflip)
               indices = getIndices(flipstate, 0)
               for index in indices:
                  if player == 1:
                     pieces = [1, -1]
                  else:
                     pieces = [2, -2]
                  for p in pieces:
                     newstate = deepcopy(flipstate)
                     newstate[index] = p
                     newnode = tree.addNode(node, newstate)
                     if maxdepth != -1:
                        if newnode.depth < maxdepth:
                           recurse(newnode, nextPlayer)
                     else:
                        recurse(newnode, nextPlayer)
      else:
         indices = getIndices(state, 0)
         for index in indices:
            if player == 1:
               pieces = [1, -1]
            else:
               pieces = [2, -2]
            for p in pieces:
               newstate = deepcopy(state)
               newstate[index] = p
               newnode = tree.addNode(node, newstate)
               if maxdepth != -1:
                  if newnode.depth < maxdepth:
                     recurse(newnode, nextPlayer)
               else:
                  recurse(newnode, nextPlayer)

   recurse(tree.root, rootPlayer)


def matchFilters(state):
   '''Check the state against all of the filters.  Return True if there is a match'''
   #print(state)
   correctFilters = {}
   for f in filters:
      #print(f)
      result = []
      #print(len(f))
      for i in range(len(f)):
         if f[i] == 1:
            #print(str(f[i]) + ", " + str(state[i]))
            result.append(state[i])
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
   
def endState(state):
   '''Return True if this state is an end state'''
   #print("CHECK END STATE")
   filterDict = matchFilters(state)
   #print("FDict: " + str(filterDict))
   #print(len(filterDict) == 0)
   if len(filterDict) != 0:
      for key in filterDict.keys():
         for f in filterDict[key]:
            #print(f)
            indices = getIndices(f, 1)
            #print(indices)
            F = getValidFlipLocations(state, indices)
            #print(F)
            is_end_state = True
            for k in F.keys():
               if len(F[k]) > 0:
                  is_end_state = False
            if is_end_state:
               return True
   else:
      #print("Hello")
      indices = getIndices(state, 0)
      #print(indices)
      if len(indices) == 0:
         return True
   return False
   
def getWinners(state):
   '''Assuming the state is an end state, get a list of winners.  Can have the same winner multiple times if the winner has multiple winning lines.'''
   filterDict = matchFilters(state)
   if len(filterDict) != 0:
      #print(filterDict)
      winners = {}
      for key in filterDict.keys():
         if abs(key) not in winners:
            winners[abs(key)] = 1
         else:
            winners[abs(key)] += 1
      return winners

   return None

   
def getRandomState(state, player):
   '''Return a random next state which includes a random flip and a random placement.  Need to get all possibilities before choosing a random one.'''
   #print("")
   #print("----------------------------------")
   #print(state)
   indicesOP = indicesOfOtherPlayer(state, player)
   flipIndices = getValidFlipLocations(state, indicesOP)
   #print("FlipIndices: " + str(flipIndices))
   
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
      flipstate = getFlipState(state, keys[ikey], flipindex)
      #print(flipstate)
      #print("==============================")
      indices = getIndices(flipstate, 0)
      #print("Zero indices: " + str(indices))
      index = randint(0, len(indices)-1)
      iplayer = randint(0,1)
      if player == 1:
         p = [1,-1][iplayer]
      else:
         p = [2,-2][iplayer]
         
      newstate = deepcopy(flipstate)
      newstate[indices[index]] = p
      return newstate, None

   else:
      indices = getIndices(state, 0)
      index = randint(0, len(indices)-1)
      iplayer = randint(0,1)
      if player == 1:
         p = [1, -1][iplayer]
      else:
         p = [2, -2][iplayer]
      newstate = deepcopy(state)
      newstate[index] = p
      return newstate, index
      
         
def montecarlo(state, player):
   '''Make random decisions all the way to an end state'''
   turns = 0
   firstMove = True
   firstMoveState = [] 
   while not endState(state):
      state, fmi = getRandomState(state, player)
      player = getNextPlayer(player)
      #print(state)
      turns += 1
      if firstMove:
         firstMoveState = state 
      firstMove = False
      
   #print("++++++++++++++++++++++++++++++++")
   #print(state)
   #print("WINNERS")
   #print(getWinners(state))
   #print(str(turns) + " turns")
   winners = getWinners(state)
   return firstMoveState, turns, winners



#================================================================
player = 1
print("TESTING")
#state = [1,-1,2,1,1,2,1,2,1,-2,2,2,0,0,0,0]
#print(endState(state))
      
      
state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while not endState(state):
   allstates = []
   allturns = []
   allwinners = []
   for i in range(500):
      moveState, turns, winners = montecarlo(state, player)
      allstates.append(moveState)
      allturns.append(turns)
      allwinners.append(winners)
      #print(str(moveIndex) + ", " + str(turns))

   #print("Player " + str(player))
   #print(allstates)
   #print("")
   #print(allturns)
   #print("")
   #print(allwinners)

   allstatesFiltered = []
   allturnsFiltered = []
   allwinnersFiltered = []

   for i in range(len(allwinners)):
      if player == 1: otherplayer = 2
      else: otherplayer = 1

      if allwinners[i] is not None:
         if otherplayer not in allwinners[i].keys():
            allwinnersFiltered.append(allwinners[i])
            allstatesFiltered.append(allstates[i])
            allturnsFiltered.append(allturns[i])

   #print("")
   #print("")
   #print(allstatesFiltered)
   #print("")
   #print(allturnsFiltered)
   #print("")
   #print(allwinnersFiltered)


   Dindices = {}
   for i in range(len(allturnsFiltered)):
      if allturnsFiltered[i] not in Dindices:
         Dindices[allturnsFiltered[i]] = [i]
      else:
         Dindices[allturnsFiltered[i]].append(i)

   #print("")
   #print(Dindices)

   lowestKey = min(Dindices.keys())
   print("Player "+ str(player)+"'s best move can win in " + str(lowestKey) + " moves")
   state = allstatesFiltered[Dindices[lowestKey][0]]
   print(state)
   if player == 1: player = 2
   else: player = 1



"""
state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)
print(endState(state))

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)
print(endState(state))

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)
print(endState(state))

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)
print(endState(state))

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)
print(endState(state))

state = getRandomState(state, player)
player = getNextPlayer(player)
print(state)
print(endState(state))

#tree = Tree()
#tree.root.data = startState

#player = 1 #value for player 2 is 2
#montecarlo(startState, player)
#constructTree(player, 4)
#n = tree.walk(0, tree.root)
#print(n)



tree = Tree()
tree.addNode(tree.root, 9)
tree.addNode(tree.root, 10)
tree.addNode(tree.root, 11)
tree.addNode(tree.root.children[0], 4)
tree.addNode(tree.root.children[0], 6)
tree.addNode(tree.root.children[1], 8)
tree.addNode(tree.root.children[1], 1)
tree.addNode(tree.root.children[2], 7)
tree.addNode(tree.root.children[2], 90)
tree.addNode(tree.root.children[2], 66)
tree.addNode(tree.root.children[0].children[1], 78)
tree.addNode(tree.root.children[0].children[1], 99)

#tree.walk(0, tree.root)

minimax = Minimax(tree)
index = minimax.findBestMove('X')
print("INDEX TO BEST SCORE: " + str(index))
"""
