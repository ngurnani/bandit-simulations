"""
Created on May 2, 2013

This script contains all the useful sidefunctions for studying
the Maximum Weighted Spanning Tree problem in the Combinatorial
Identification Setting.

@author: ngurnani
"""

import os
os.getcwd()
os.chdir('/Users/ngurnani/Dropbox/Senior/Thesis/Code')
from math import*
from pandas import DataFrame as df
import networkx as nx
import time
import xlwt
from scipy.stats import bernoulli


"""
Simple function to copy list to excel spreadsheet
"""
def copyToExcel(result):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    
    for i,e in enumerate(result):
        sheet1.write(i,1,e)
    
    name = "random.xls"
    book.save(name)
    
"""        
Function caclculates sample Max Weighted Bipartite Matching
NOT FINISHED YET - ngurnani (05/02/13)            
"""                
def calcMaxBip(V,empirical_means):
    # Every time a new complete bipartite graph is constructed here.
    G=nx.complete_bipartite_graph(V,V)  #N.B. Indexing from 0 to K-1 
    
    edges=list(G.edges_iter())
    for (u,v) in edges:
        # assign negative weights so that MST calculates MaxST
        G.add_edge(u,v,weight=-(empirical_means[edges.index((u,v))]))     
    
    T = nx.max_weight_matching(G)
    temp=T.edges()
    output=[0]*len(temp)
    for indx in range(len(output)):
        output[indx]=edges.index(temp[indx])
    
    return output # Indices are from 0 to K-1    
                                                                       
"""
Function runs Kruskal to calculate sample Max Weighted Spanning Tree
NOTE: BE CAREFUL AS TO HOW EMPIRICAL MEANS ARE SYSTEMATICALLY ASSIGNED
""" 
def calcMaxST(V,empirical_means):
    # Every time a new complete graph is constructed here.
    G=nx.complete_graph(V)  #N.B. Indexing from 0 to K-1 
    
    edges=list(G.edges_iter())
    for (u,v) in edges:
        # assign negative weights so that MST calculates MaxST
        G.add_edge(u,v,weight=-(empirical_means[edges.index((u,v))]))     
    
    T = nx.minimum_spanning_tree(G)
    temp=T.edges()
    output=[0]*len(temp)
    for indx in range(len(output)):
        output[indx]=edges.index(temp[indx])
    
    return output # Indices are from 0 to K-1    

"""
Function orders the empirical means into two sets those belonging to T^ and ~T^ and returns ordered Arms
"""
def orderT_Arm(sample_T,empirical_means):
    
    temp1 = [empirical_means[i] for i in sample_T]
    dict1 = dict(zip(sample_T,temp1)) 
    order1 = list(sorted(dict1,key=dict1.__getitem__,reverse=True))

    indx_empirical_means=list(xrange(len(empirical_means)))
    [indx_empirical_means.remove(j) for j in sample_T]
    temp2= [empirical_means[i] for i in indx_empirical_means]
    dict2= dict(zip(indx_empirical_means,temp2))
    order2= list(sorted(dict2,key=dict2.__getitem__,reverse=True))   
    
    return order1 + order2

"""
Function orders the empirical means into two sets those belonging to T^ and ~T^
"""
def orderT(sample_T,empirical_means):
    temp1 = [empirical_means[i] for i in sample_T]
    order1 = sorted(temp1,reverse=True)

    indx_empirical_means=list(xrange(len(empirical_means)))
    [indx_empirical_means.remove(j) for j in sample_T] # CHECK THIS LINE STILL WORKS
    temp2= [empirical_means[i] for i in indx_empirical_means]
    order2 = sorted(temp2,reverse=True)
    
    return order1 + order2
 
"""
Returns a list of Bernoulli parameters corresponding to experiment inputted
"""
def oracle_means(experiment):
    if experiment==1:
        return [0.5] + [0.4]*20 # V = 7, K = 21
    elif experiment==2:
        return [0.5] + [0.42]*5 + [0.38]*15 # V = 7, K = 21
    elif experiment==3:
        return [0.5, 0.49743427, 0.4930656,0.48125839, 0.449347, 0.3631] # V = 4, K = 6
    elif experiment==4:
        return [0.5,0.42,0.4,0.4,0.35,0.35] # V = 4, K = 6
    elif experiment==5:
        return [0.5] + [(0.5-(0.025*j)) for j in range(2,16)] # V = 6, K = 15
    elif experiment==6:
        return [0.5] + [0.45]*7 + [0.43]*14 + [0.38]*14 # V = 9, K = 36

"""
Returns a list of edges corresponding to experiment inputted
"""
def oracle_set(experiment):
    if experiment==1:
        return [0,1,2,3,4,5] # V = 7, K = 21
    elif experiment==2:
        return [0,1,2,3,4,5] # V = 7, K = 21
    elif experiment==3:
        return [0,1,2] # V = 4, K = 6
    elif experiment==4:
        return [0,1,2] # V = 4, K = 6
    elif experiment==5:
        return [0,1,2,3,4] # V = 6, K = 15
    elif experiment==6:
        return [0,1,2,3,4,5,6,7] # V = 9, K = 36
        
"""
Function calculates the value of log_K
"""
def log_SAR(K):
    extra_sum=0
    for j in range(2,K+1):
        extra_sum = extra_sum + (1.0/j)
    log_K=0.5+extra_sum
    return log_K

"""
Function calculates the number of rounds of SAR
"""
def rounds_SAR(n,K,alpha):
    if alpha==0:
        return 0.0
    a = 1.0/log_SAR(K)
    b = float((n-K))/((K+1)-alpha)
    return ceil(a*b)  
    
"""
Calculates hardness measure (as defined in Bubeck et. al 2013) for given gaps
"""
def hardness(empirical_gaps):
    runsum = 0.0
    for val in empirical_gaps:
        if val!= 0.0:
            runsum = runsum + (1/(val*val)) 
    return runsum
      