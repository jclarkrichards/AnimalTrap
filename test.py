from tree import Tree
from copy import deepcopy

NUMROWS = 4
NUMCOLS = 4

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
      D[val] = [k for k in adjacents if S[k] == 0]
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
         for i in flipIndices.keys():
            for iflip in flipIndices[i]:
               flipstate = getFlipState(state, i, iflip)
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

   
def montecarlo():
   '''Make random decisions all the way to an end state'''
   pass


   
startState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
tree = Tree()
tree.root.data = startState

player = 1 #value for player 2 is 2
constructTree(player, 4)
n = tree.walk(0, tree.root)
print(n)


"""
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
