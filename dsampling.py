import math
from random import choices

class DSampling:
    def __init__(self, px0):
        #cpt tables 1d and 2d
        self.probXEqualsZero = px0 

    def get_Sample(self, values, probabilities):
        """Pass 2 lists, first with all possible values and secind with corresponding probabilities to get a randomly sampled value."""
        return choices(values,probabilities)
    
    def get_Key(self, *k):
        return ''.join(str(e) for e in k)

        
class ChainSampling(DSampling):
    def __init__(self, px0, length):
        DSampling.__init__(self, px0)
        self.chainLength = length
        self.two_row_cpt = {"0":0.95, "1":0.05}
    
    def get_Parent(self, node):
        return node-1   


class TreeSampling(DSampling):
    def __init__(self, px0, levels):
        DSampling.__init__(self, px0)
        self.treeLevels = levels        
        self.two_row_cpt = {"0":0.95, "1":0.05}
    
    def get_Parent(self, node):
        return math.floor(node/2)


class GridSampling(DSampling):
    def __init__(self, px0, n):
        DSampling.__init__(self, px0)
        self.grid_Size = n
        self.two_row_cpt = {"0":0.95, "1":0.05}
        self.four_row_cpt = {"00":0.99, "01":0.5, "10":0.5, "11":0.01}
    
    def get_Parent(self, node):
        if(node <= self.grid_Size):
            return node-1            
        elif((node-1)%self.grid_Size == 0):
            return node-self.grid_Size
        else:
            return (node-self.grid_Size, node-1) 

# num2=sum((GLarge.df['x6']==1) &(GLarge.df['x64']==0))