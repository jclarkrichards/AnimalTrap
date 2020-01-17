from tree import Tree
from copy import deepcopy
from random import randint
from constants import *
from utils import *
from gamerules import AnimalTrap


"""
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
"""

#================================================================
print("TESTING")
#state = [1,-1,2,1,1,2,1,2,1,-2,2,2,0,0,0,0]
#print(endState(state))
game = AnimalTrap()
#print(game.state.endState())
#print(game.state.getWinners())

print("........................")
game.setNextStateAuto()
print("Chosen state")
print(game.state)

print("........................")
#game.state = state
game.setNextStateAuto()
print("Chosen state")
print(game.state)

print("........................")
#game.state = state
game.setNextStateAuto()
print("Chosen state")
print(game.state)

print("........................")
#game.state = state
game.setNextStateAuto()
print("Chosen state")
print(game.state)




print(game.state)
print("")
print("")
print("")
#state = game.state.copy()

#game.setPlayer()
#print("Player " + str(game.player))
#game.state = game.getRandomState(game.state)
#print(game.state)
#print(game.state.endState())












"""
while not game.state.endState(state):
   allstates = []
   allturns = []
   allwinners = []
   for i in range(50):
      moveState, turns, winners = game.montecarlo()
      allstates.append(moveState)
      allturns.append(turns)
      allwinners.append(winners)

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
