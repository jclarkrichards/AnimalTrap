"""This is a representation of a tree.  A tree has a root node, and each node can have numerous children.  Children have parents except for the root node.  A child can only have 1 parent."""
class TreeNode(object):
    def __init__(self):
        self.id = [] #each Node object is unique
        self.parent = None
        self.children = []
        self.data = None #GameState object
        self.score = 0
        self.depth = 0
        
    def __repr__(self):
        return "Node: " + str(self.id)

    
class Tree(object):
    def __init__(self):
        self.root = TreeNode()
        self.root.id = [0]

    def findNode(self, id):
        '''Find the node in the tree with the given id.  The id shows the path the tree must take to reach the desired node.'''
        node = self.root
        vals = id[len(self.root.id):]
        for val in vals:
            try:
                node = node.children[val]
            except IndexError:
                return None
        return node

    def find(self, data):
        '''If you have the data instead of the id.  Return TreeNode object.'''
        def recurse(node):
            #print(str(data) + ", " + str(node.data))
            if data == node.data:
                return node
            for n in node.children:
                anode = recurse(n)
                if anode is not None: return anode
            return None
        return recurse(self.root)
    
    def addNode(self, parent, data=None):
        '''Add a node to the tree.  This node should be a child of the given parent node'''
        node = TreeNode()
        node.data = data
        for val in parent.id:
            node.id.append(val)
        node.parent = parent
        numchildren = len(parent.children)
        node.id.append(numchildren)
        node.depth = len(node.id)-1
        parent.children.append(node)
        return node
    
    def walk(self, num, node):
        '''Walk through the tree and print out all of the nodes, print leaves first'''
        if len(node.children) == 0:
            num += 1
            print("L: " + str(node) + " depth: " + str(node.depth) + " score: " + str(node.score))
            print(node.data)
        else:
            for n in node.children:
                num = self.walk(num, n)
            #print("N: " + str(node) + " depth: " + str(node.depth) + " score: " + str(node.score))
            #print(node.data)

        return num
    
    def isLeaf(self, id):
        '''Check if the node with the given id is a leaf or not'''
        node = self.findNode(id)
        if len(node.children) == 0:
            return True
        return False

    def prune(self, node, filters):
        '''Prune the tree so that nodes with a 3-in-a-row have no children'''
        if node.data.isEndState(filters):
            node.children = []  #empty the children
            node.data.setWinner(filters)
        else:
            for n in node.children:
                self.prune(n, filters)
    
    def setRoot(self, id):
        '''Given an id, set that node as the root.  This removes portions of the tree'''
        node = self.findNode(id)
        if node is not None:
            self.root = node
            self.root.parent = None
            self.decreaseDepth()
            
    def decreaseDepth(self):
        '''Go through tree and set the depth of all nodes to 1 less than previous'''
        def recurse(node):
            node.depth -= 1
            for childNode in node.children:
                recurse(childNode)
        recurse(self.root)
        
    #set root with data as well instead of id
    def checkWinners(self, node, wins, symbol):
        if len(node.children) == 0:
            if node.data.winner == symbol:
                wins[node.depth] += 1
        else:
            for n in node.children:
                wins= self.checkWinners(n, wins, symbol)

        return wins
