#!/usr/bin/env python
# coding: utf-8

# In[126]:


import math
import pandas as pd
import numpy as np

class DSampling:
    def __init__(self,root,CPT,N):
        self.N=N
        self.df=pd.DataFrame()
        self.Column=[]
        self.root=root
        self.CPT=CPT
        for i in range(self.N):
            self.Column.append('x'+str(i+1))
        
    
    def Sampling(self):
        pass
        

    
class ChainSampling(DSampling):
    def __init__(self,root,CPT,N):
        super().__init__(root,CPT,N)
        
    
    def Sampling(self):
        #Root
        Root=np.empty((0),dtype=int)
        for i in range(10):
            choice=np.random.choice(np.arange(0,2),p=self.root)
            Root=np.append(Root,choice)
        self.df['x1']=Root
        
        
        for var in self.Column[1:]:
            X=np.empty((0),dtype=int)
            for pc in self.df.iloc[:,-1]:
                P=self.CPT[pc]
                choice=np.random.choice(np.arange(0,2),p=P)
                X=np.append(X,choice)
            self.df[var]=X
        
class TreeSampling(DSampling):
    def __init__(self,root,CPT,N):
        super().__init__(root,CPT,N)
    
    
    def Sampling(self):
        #Root
        Root=np.empty((0),dtype=int)
        for i in range(100000):
            choice=np.random.choice(np.arange(0,2),p=self.root)
            Root=np.append(Root,choice)
        self.df['x1']=Root
        
        node=2
        for var in self.Column[1:]:
            X=np.empty((0),dtype=int)
            parent='x'+str(math.floor(node/2))
            node+=1
            
            for pc in self.df[parent]:
                P=self.CPT[pc]
                choice=np.random.choice(np.arange(0,2),p=P)
                X=np.append(X,choice)
            self.df[var]=X
    
    

class GridSampling(DSampling):
    def __init__(self,root,CPT,N):
        super().__init__(root,CPT,N)
        
    def Sampling(self):
        #Root
        Root=np.empty((0),dtype=int)
        for i in range(100000):
            choice=np.random.choice(np.arange(0,2),p=self.root)
            Root=np.append(Root,choice)
        self.df['x1']=Root
        
        
        node=2
        for var in self.Column[1:]:
            # Finding the parent
            gridSize=int(math.sqrt(self.N))

            if(node <= gridSize): #first column
                parent=node-1           
            elif((node-1)%gridSize == 0):
                parent=node-gridSize
            else:
                parent=(node-gridSize, node-1)
                
            X=np.empty((0),dtype=int)
            node+=1
            
            

            if isinstance(parent,tuple):
                p1='x'+str(parent[0])
                p2='x'+str(parent[1])

                for p1c,p2c in zip(self.df[p1].values,self.df[p2].values):
                    P=self.CPT['Two'][(p1c,p2c)]
                    choice=np.random.choice(np.arange(0,2),p=P)
                    X=np.append(X,choice)
            else:
                parent='x'+str(parent)
                for pc in self.df[parent]:
                    P=self.CPT['One'][pc]
                    choice=np.random.choice(np.arange(0,2),p=P)
                    X=np.append(X,choice)
            self.df[var]=X

    


# In[127]:


def main():
    CPT_G={
        'One':
        {
            0:[0.95,0.05],
            1:[0.05,0.95]
        },

        'Two':
        {
            (0,0):[0.99,0.01],
            (0,1):[0.5,0.5],
            (1,1):[0.05,0.95],
            (1,0):[0.5,0.5]
        }

    }
    root=[0.05,0.95]
    N=16
    
    #Call Grid
    G=GridSampling(root,CPT_G,N)
    G.Sampling()
    print(G.df)
    
    #Call Tree
    CPT={
        0:[0.95,0.05],
        1:[0.05,0.95]
    }
    root=[0.05,0.95]
    N=7
    
    T=TreeSampling(root,CPT,N)
    T.Sampling()
    print(T.df)
    
    #For counting x1=1 and x2=1: T.df['x1'].value_counts()[1] and T.df['x2'].value_counts()[1]
 


# In[ ]:


main()

