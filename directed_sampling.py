import math
from random import choices
import numpy as np

class DSampling:
    def __init__(self, px0, nodes,samples):
        #cpt tables 1d and 2d
        self.root_probability = px0
        self.nodes=nodes
        self.number_of_samples=samples
        self.samples=np.empty([self.number_of_samples, self.nodes], dtype=int) 
        self.possible_states=[0,1]

        for i in range(self.number_of_samples):
            self.samples[i][0]=self.get_Sample(self.possible_states, self.root_probability)[0]
            # self.samples[i][0]=self.get_Sample(self.possible_states, self.root_probability)

    def get_Sample(self, values, probabilities):
        """Pass 2 lists, first with all possible values and second with corresponding probabilities to get a randomly sampled value."""
        return choices(values,probabilities)
        # return np.random.choice(values,p=probabilities)
    
    # def get_Key(self, *k):
    #     return ''.join(str(e) for e in k)

    def get_Mask(self, vars, flag):
        mask=np.zeros((self.nodes,), dtype=int)
        # print(f'gm {vars}')
        for k,v in vars.items():
            if(v==1):
                mask[k-1]=1
            elif(flag==0 and v==0):
                mask[k-1]=1
        return mask

    def get_matching_sample_count(self, query):
        # query_mask=self.get_Mask(query,0)
        # check_mask=self.get_Mask(query,1)
        # print(f'qm {query_mask}')
        # print(f'cm {check_mask}')
        count=0
        for i in range(self.samples.shape[0]):
            # if np.array_equiv(np.bitwise_and(self.samples[i], query_mask),check_mask):
            #     count+=1
            flag=True
            for k,v in query.items():
                if(self.samples[i][k-1]!=v):
                    flag=False
                    break
            if flag:
                count+=1                    
        return count

    def get_probability(self, query, evidence={}):
        query.update(evidence)
        num = self.get_matching_sample_count(query)        
        den = self.number_of_samples if not evidence else self.get_matching_sample_count(evidence)
        # print(num, den)
        return num/den

    def print_Head(self):
        for i in range(5):
            for j in range(self.samples.shape[1]):
                print(f'{self.samples[i][j]} ', end='')
            print()
        
class ChainSampling(DSampling):
    def __init__(self, px0, nodes, samples):
        DSampling.__init__(self, px0, nodes,samples)
        self.cpt = [[0.95, 0.05], [0.05, 0.95]]    

    def get_Parent(self, node):
        return node-1

    def do_Sampling(self):
        for node in range(1,self.nodes):
            parent_node = self.get_Parent(node)
            for sample in range(self.number_of_samples):  
                previous_state=self.samples[sample][parent_node]              
                self.samples[sample][node]=self.get_Sample(self.possible_states, self.cpt[int(previous_state)])[0]
                # self.samples[sample][node]=self.get_Sample(self.possible_states, self.cpt[int(previous_state)])
    

class TreeSampling(DSampling):
    def __init__(self, px0, nodes, samples):
        DSampling.__init__(self, px0, nodes, samples)
        self.cpt = [[0.95, 0.05], [0.05, 0.95]]   
    
    def get_Parent(self, node):
        return math.floor((node-1)/2)

    def do_Sampling(self):
        for node in range(1,self.nodes):
            parent_node = self.get_Parent(node)
            for sample in range(self.number_of_samples):  
                previous_state=self.samples[sample][parent_node]              
                self.samples[sample][node]=self.get_Sample(self.possible_states, self.cpt[int(previous_state)])[0]
                # self.samples[sample][node]=self.get_Sample(self.possible_states, self.cpt[int(previous_state)])


class GridSampling(DSampling):
    def __init__(self, px0, nodes, samples):
        DSampling.__init__(self, px0, nodes, samples)
        self.grid_Size = int(math.sqrt(nodes))
        # print(f'gS= {self.grid_Size}')
        self.cpt = [[0.95, 0.05], [0.05, 0.95]]   
        self.four_row_cpt = [[0.99,0.01],
                             [0.5,0.5],
                             [0.5,0.5],
                             [0.01,0.99]]
    
    def get_Parent(self, node):
        if(node < self.grid_Size):
            return node-1            
        elif((node%self.grid_Size) == 0):
            return node-self.grid_Size
        else:
            return (node-self.grid_Size, node-1) 

    def do_Sampling(self):
        for node in range(1,self.nodes):
            parent_node = self.get_Parent(node)
            # print(f'parent= {parent_node} {type(parent_node)}')
            for sample in range(self.number_of_samples):
                if isinstance(parent_node,tuple):     
                    previous_state_j=self.samples[sample][parent_node[0]]   
                    previous_state_k=self.samples[sample][parent_node[1]]
                    previous_state=(previous_state_j * 2**1) + (previous_state_k * 2**0) 
                    # print(previous_state_j, previous_state_k, previous_state)   
                    # print(f'if {previous_state}')
                    self.samples[sample][node]=self.get_Sample(self.possible_states, self.four_row_cpt[int(previous_state)])[0] 
                    # self.samples[sample][node]=self.get_Sample(self.possible_states, self.four_row_cpt[int(previous_state)])

                else:
                    # print("else")
                    previous_state=self.samples[sample][parent_node]            
                    self.samples[sample][node]=self.get_Sample(self.possible_states, self.cpt[int(previous_state)])[0] 
                    # self.samples[sample][node]=self.get_Sample(self.possible_states, self.cpt[int(previous_state)]) 

def driver():
    samples_to_draw=100000

    C=ChainSampling([0.05, 0.95], 16, samples_to_draw)
    C.do_Sampling()
    print("\nChain::")
    print(C.get_probability({5:1}))
    print(C.get_probability({5:1}, {1:1}))
    print(C.get_probability({5:1}, {1:1, 10:1}))
    print(C.get_probability({5:1}, {1:1, 10:1, 15:0}))

    T=TreeSampling([0.05, 0.95], 15, samples_to_draw)
    T.do_Sampling()
    print("\nTree small::")
    print(T.get_probability({8:1}))
    print(T.get_probability({8:1}, {12:1}))
    print(T.get_probability({8:1}, {12:1, 7:1}))
    print(T.get_probability({8:1}, {12:1, 7:1, 15:0}))

    T=TreeSampling([0.05, 0.95], 63, samples_to_draw)
    T.do_Sampling()
    print("\nTree large::")
    print(T.get_probability({32:1})) 
    print(T.get_probability({32:1}, {45:1})) 
    print(T.get_probability({32:1}, {45:1, 31:1}))
    print(T.get_probability({32:1}, {45:1, 31:1, 63:0}))

    G=GridSampling([0.5, 0.5], 16, samples_to_draw)
    G.do_Sampling()
    print("\nGrid small::")
    print(G.get_probability({6:1}))
    print(G.get_probability({6:1}, {16:0}))
    print(G.get_probability({6:1}, {16:0, 1:0}))
    print(G.get_probability({6:1}, {16:0, 1:0, 15:0}))    
    # G.print_Head()

    G=GridSampling([0.5, 0.5], 64, samples_to_draw)
    G.do_Sampling()
    print("\nGrid large::")
    print(G.get_probability({6:1}))
    print(G.get_probability({6:1}, {64:0}))
    print(G.get_probability({6:1}, {64:0, 1:0}))
    print(G.get_probability({6:1}, {57:0, 58:0, 59:0, 60:0, 61:0, 62:0, 63:0, 64:0})) 

def main():
    for i in range(5):
        print(f'\n\nRound {i+1}')
        driver()
   

main()
