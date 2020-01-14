from minimax import Minimax
from tree import Tree
from tictactoe import TicTacToe
from copy import deepcopy

#game = TicTacToe()
#game.startState = ['X','O', 'X', -1, 'X', -1, -1, 'O', -1]
#game.setupTree()
#num = game.tree.walk(0, game.tree.root)
#print(num)


startState = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
tree = Tree()
tree.root.data = startState
def constructTree(maxdepth):
   def recurse(node):
      state = deepcopy(node.data)
      numFreeSpots = len([k for k in state if k == -1])
      indices = []
      for i in range(len(state)):
         if state[i] == -1:
            indices.append(i)
      for index in indices:
         newstate = deepcopy(state)
         if (numFreeSpots % 2) == 0:
            newstate[index] = 'X'
         else:
            newstate[index] = 'O'
         newnode = tree.addNode(node, newstate)
         if newnode.depth < maxdepth:
            recurse(newnode)
           
   recurse(tree.root)

constructTree(4)
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
