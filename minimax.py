"""Minimax algorithm needs to have a tree in order to work.  """

class Minimax(object):
    def __init__(self, tree):
        self.tree = tree

    def findBestMove(self, playerSymbol):
        '''Given a player symbol, return the index to the best child in the trees root (best move that this player should make'''
        #traverse down tree until you find a leaf
        #when you find a leaf give it a score based on the symbol
        #for example, if this symbol is 'X' and the leaf shows that 'X' is the
        #winner, then give it a positive score.  If 'O' is the winner, then
        #give it a negative score.  0 if tie.
        #When you visit all children of a node, then get the best score
        #from the children depending on the depth
        #If the depth is even then get the largest value from children.
        #If the depth is odd then get the smallest value from the children.
        #When you reach the root and all children have been visited,
        #return the index of the child that corresponds to the score received.
        #the only modifications we do on the tree here is giving the
        #tree states a score.
        def recurse(node):
            if len(node.children) == 0:
                self.scoreChild(node, playerSymbol)
                #print("leaf node : " + str(node.data) + " has score " + str(node.score))
            else:
                for childnode in node.children:
                    recurse(childnode)
                self.getBestScoreFromChildren(node)
                #print("Parent: " + str(node.data) + " has score " + str(node.score))
                
        recurse(self.tree.root)
        return self.indexOfBestScore(self.tree.root)

    def scoreChild(self, node, symbol):
        '''Find the winner of this end node if any.  If the same as the symbol,
        then give it a positive score.  Divide score by depth'''
        #print("Giving child a score at depth " + str(node.depth))
        #node.score = node.data / float(node.depth)
        #winner = node.state.getWinner()
        if node.data.winner is not None:
            if node.data.winner == symbol:
                node.score = 1.0 / float(node.depth)
            else:
                node.score = -1.0 / float(node.depth)
        else:
            node.score = 0
        
    def getBestScoreFromChildren(self, node):
        '''Set the score for this node based on the depth of this node'''
        scores = []
        for child in node.children:
            scores.append(child.score)
            
        if node.depth % 2 == 0:
            node.score = max(scores)    
        else:
            node.score = min(scores)
        #print("Score for node is: " + str(node.score))
        
    def indexOfBestScore(self, node):
        '''Return the index of the child with the best score'''
        scores = []
        for child in node.children:
            scores.append(child.score)
        print(scores)
        return scores.index(max(scores))

    
