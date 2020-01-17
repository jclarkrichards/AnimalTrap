"""Utils describes methods that are not specific to any particular game.  These are general methods that could be applied to many different applications."""
from constants import *

#L=[1,5,4,1,0,1] val=1, return [0,3,5]
def getIndicesFromValue(L, val):
    indices = []
    for i in range(len(L)):
        if L[i] in val:
            indices.append(i)
    return indices

#L=[1,5,4,1,0,1] val=[1,5], return [0,1,3,5]
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

#Assuming a square grid:  if index=5, return 1 if NUMROWS=4
# 0 | 1 | 2 | 3                                                                
# - + - + - + -                                                                
# 4 | 5 | 6 | 7                                                                
# - + - + - + -                                                                
# 8 | 9 | 10| 11                                                               
# - + - + - + -                                                                
# 12| 13| 14| 15 
def getRow(index):
    '''Given an index, return the row number'''
    return index / NUMROWS

def getColumn(index):
    '''Given an index, return the column number'''
    return index % NUMCOLS

def getIndexFromRowCol(row, column):
    '''Given a row and column value, return the index'''
    #print("r="+str(row) + ", c="+str(column))                                 
    if row >= 0 and row < NUMROWS:
        if column >= 0 and column < NUMCOLS:
            return row*NUMCOLS + column
    return None

#if val is 7, return [3, 6, 11]
def getAdjacentIndices(S, val): #don't need S
    '''Return a list of adjacent indices to val in S'''
    row = getRow(val)
    column = getColumn(val)
    indices = []
    indices.append(getIndexFromRowCol(row+1, column))
    indices.append(getIndexFromRowCol(row-1, column))
    indices.append(getIndexFromRowCol(row, column+1))
    indices.append(getIndexFromRowCol(row, column-1))
    return [k for k in indices if k is not None]

#L=[0,6,14], return {0:[1,4], 6:[2,5,7,10], 14:[10,13,15]}
def getValidFlipLocations(S, L):
    '''Given the state S and a list of indices L, return a dictionary where    
   each entry in L is a key and the values are a list of adjacent indices. From that list of adjacent indices, only include the indices that are empty.'''
    D = {}
    for val in L:
        adjacents = getAdjacentIndices(S, val)
        #print("Adjacents: " + str(adjacents))   
        empty = [k for k in adjacents if S[k] == 0]
        if len(empty) > 0:
            D[val] = empty
    return D
