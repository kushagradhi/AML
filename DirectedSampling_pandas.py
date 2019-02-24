#TO-DO: Refactor query/evidence nodes handling
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
        for i in range(100000):
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
        print(self.df.head)
        
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
        self.no_of_samples = 100000

    def Sampling(self):
        #Root
        Root=np.empty((0),dtype=int)
        for i in range(self.no_of_samples):
            choice=np.random.choice(np.arange(0,2),p=self.root)
            Root=np.append(Root,choice)
        self.df['x1']=Root
        # print(self.df['x1'])
        
        node=2
        gridSize=int(math.sqrt(self.N))
        for var in self.Column[1:]:
            # Finding the parent
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
        # print("entire:")
        # print(self.df.head)

def calcGrid():
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
            (1,0):[0.5,0.5],
            (1,1):[0.01,0.99]
            
        }

    }
    root=[0.5,0.5]

        #Call Grid
        # G=GridSampling(root,CPT_G,16)
        # G.Sampling()
        # print(G.df.head())
        # print("G small")
        # num=len(G.df[(G.df["x6"]==1)])
        # print("x6=1  {} / {} = {}".format(num, 100000, num/100000))

        # num=len(G.df[(G.df["x6"]==1) & (G.df["x16"]==0)])
        # den=len(G.df[(G.df["x16"]==0)])
        # print("x6=1 | x16=0 {} / {} = {}".format(num, den, num/den))

        # num=len(G.df[(G.df["x6"]==1) & (G.df["x16"]==0) & (G.df["x1"]==0)])
        # den=len(G.df[(G.df["x16"]==0) & (G.df["x1"]==0)])
        # print("x6=1 | x16=0, x1=0 {} / {} = {}".format(num, den, num/den))

        # num=len(G.df[(G.df["x6"]==1) & (G.df["x16"]==0) & (G.df["x1"]==0) & (G.df["x15"]==0)])
        # den=len(G.df[(G.df["x16"]==0) & (G.df["x1"]==0) & (G.df["x15"]==0)])
        # print("x6=1 | x16=0, x1=0, x15=0 {} / {} = {}".format(num, den, num/den))


        # GLarge=GridSampling(root,CPT_G,64)
        # GLarge.Sampling()
        # print(GLarge.df.head())
        # print("G large")
        # num=len(GLarge.df[(GLarge.df["x6"]==1)])
        # print(GLarge.df.query('x6 == 1'))
        # print("x6=1  {} / {} = {}".format(num, 100000, num/100000))

        # num=len(GLarge.df[(GLarge.df["x6"]==1) & (GLarge.df["x64"]==0)])
        # den=len(GLarge.df[(GLarge.df["x64"]==0)])
        # print("x6=1 | x64=0 {} / {} = {}".format(num, den, num/den))

        # num=len(GLarge.df[(GLarge.df["x6"]==1) & (GLarge.df["x64"]==0) & (GLarge.df["x1"]==0)])
        # den=len(GLarge.df[(GLarge.df["x64"]==0) & (GLarge.df["x1"]==0)])
        # print("x6=1 | x64=0, x1=0 {} / {} = {}".format(num, den, num/den))

        # num=len(GLarge.df[(GLarge.df["x6"]==1) & (GLarge.df["x57"]==0) & (GLarge.df["x58"]==0) & (GLarge.df["x59"]==0) & (GLarge.df["x60"]==0) & (GLarge.df["x61"]==0) & (GLarge.df["x62"]==0) & (GLarge.df["x63"]==0) & (GLarge.df["x64"]==0)])
        # den=len(GLarge.df[(GLarge.df["x57"]==0) & (GLarge.df["x58"]==0) & (GLarge.df["x59"]==0) & (GLarge.df["x60"]==0) & (GLarge.df["x61"]==0) & (GLarge.df["x62"]==0) & (GLarge.df["x63"]==0) & (GLarge.df["x64"]==0)])
        # print("x6=1 | x57=..=x64=0 {} / {} = {}".format(num, den, num/den))

def main():

    for i in range(1):
        print(f'round {i+1}')
        calcGrid()
    # CPT_G={
    #     'One':
    #     {
    #         0:[0.95,0.05],
    #         1:[0.05,0.95]
    #     },

    #     'Two':
    #     {
    #         (0,0):[0.99,0.01],
    #         (0,1):[0.5,0.5],
    #         (1,1):[0.05,0.95],
    #         (1,0):[0.5,0.5]
    #     }

    # }
    # root=[0.05,0.95]
    # N=16
    


    
    
    #Call Tree
    # CPT={
    #     0:[0.95,0.05],
    #     1:[0.05,0.95]
    # }
    # root=[0.05,0.95]
    # N=7

    # T=TreeSampling(root,CPT,15)
    # T.Sampling()
    # print(T.df.head())
    # num=len(T.df[(T.df["x8"]==1)])
    # print("x8=1  {} / {} = {}".format(num, 100000, num/100000))

    # num=len(T.df[(T.df["x8"]==1) & (T.df["x12"]==1)])
    # den=len(T.df[(T.df["x12"]==1)])
    # print("x8=1 | x12=1 {} / {} = {}".format(num, den, num/den))

    # num=len(T.df[(T.df["x8"]==1) & (T.df["x12"]==1) & (T.df["x7"]==1)])
    # den=len(T.df[(T.df["x12"]==1) & (T.df["x7"]==1)])
    # print("x8=1 | x12=1, x7=1 {} / {} = {}".format(num, den, num/den))

    # num=len(T.df[(T.df["x8"]==1) & (T.df["x12"]==1) & (T.df["x7"]==1) & (T.df["x15"]==0)])
    # den=len(T.df[(T.df["x12"]==1) & (T.df["x7"]==1) & (T.df["x15"]==0)])
    # print("x8=1 | x12=1, x7=1, x15=0 {} / {} = {}".format(num, den, num/den))


    # T=TreeSampling(root,CPT,63)
    # T.Sampling()
    # print(T.df.head())
    # num=len(T.df[(T.df["x32"]==1)])
    # print("x32=1  {} / {} = {}".format(num, 100000, num/100000))

    # num=len(T.df[(T.df["x32"]==1) & (T.df["x45"]==1)])
    # den=len(T.df[(T.df["x45"]==1)])
    # print("x32=1 | x45=1 {} / {} = {}".format(num, den, num/den))

    # num=len(T.df[(T.df["x32"]==1) & (T.df["x45"]==1) & (T.df["x31"]==1)])
    # den=len(T.df[(T.df["x45"]==1) & (T.df["x31"]==1)])
    # print("x32=1 | x45=1, x31=1 {} / {} = {}".format(num, den, num/den))

    # num=len(T.df[(T.df["x32"]==1) & (T.df["x45"]==1) & (T.df["x31"]==1) & (T.df["x63"]==0)])
    # den=len(T.df[(T.df["x45"]==1) & (T.df["x31"]==1) & (T.df["x63"]==0)])
    # print("x32=1 | x45=1, x31=1, x63=0 {} / {} = {}".format(num, den, num/den))
    
    #For counting x1=1 and x2=1: T.df['x1'].value_counts()[1] and T.df['x2'].value_counts()[1]
    #len(df[(df["X1"]==0) & (df["X2"]==1)])

    # C=ChainSampling(root,CPT,15)
    # C.Sampling()
    # r1num=len(C.df[(C.df["x5"]==1)])
    # print("x5=1  {} / {} = {}".format(r1num, 100000, r1num/100000))
    # num=len(C.df[(C.df["x5"]==1) & (C.df["x1"]==1)])
    # den=len(C.df[(C.df["x1"]==1)])
    # print("x5=1 | x1=1 {} / {} = {}".format(num, den, num/den))
    # num=len(C.df[(C.df["x5"]==1) & (C.df["x1"]==1) & (C.df["x10"]==1)])
    # den=len(C.df[(C.df["x1"]==1) & (C.df["x10"]==1)])
    # print("x5=1 | x1=1, x10=1 {} / {} = {}".format(num, den, num/den))
    # num=len(C.df[(C.df["x5"]==1) & (C.df["x1"]==1) & (C.df["x10"]==1) & (C.df["x15"]==0)])
    # den=len(C.df[(C.df["x1"]==1) & (C.df["x10"]==1) & (C.df["x15"]==0)])
    # print("x5=1 | x1=1, x10=1, x15=0 {} / {} = {}".format(num, den, num/den))
    
main()

    # For counting x1=1 and x2=1: T.df['x1'].value_counts()[1] and T.df['x2'].value_counts()[1]
    # len(df[(df["X1"]==0) & (df["X2"]==1)])