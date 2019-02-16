import math

class DSampling:
    def __init__(self):
        #cpt tables 1d and 2d
        pass
    

    
class ChainSampling(DSampling):
    def __init__(self):
        DSampling.__init__(self)
    
    def getParent(self, node):
        return node-1   


class TreeSampling(DSampling):
    def __init__(self):
        DSampling.__init__(self)
    
    def getParent(self, node):
        return math.floor(node/2)


class GridSampling(DSampling):
    def __init__(self, n):
        DSampling.__init__(self)
        self.gridSize = n
    
    def getParent(self, node):
        if(node <= self.gridSize):
            return node-1            
        elif((node-1)%self.gridSize == 0):
            return node-self.gridSize
        else:
            return (node-self.getParent, node-1) 
