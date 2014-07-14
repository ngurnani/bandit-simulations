"""
Created on May 2, 2013

This is a script for a variation of the SR Algorithm to find a Maximum Weighted Spanning Tree
on a complete graph.

In this variation we do not accept any arms and when rejecting we do not remove them from the final accepted set
,we merely stop sampling them further.
    
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
import operator 
from scipy.stats import bernoulli
from MaxST_sidefunctions import *

"""
Quick and Dirty function to compute values (need to implement proper dataframe structure later)
"""
def quickSolSR(V,experiment,T,n_index):
    start_time = time.time()        
    #n_index = range(100,10001,100)
    result = [0]*len(n_index)
    for n in n_index:
        result[n_index.index(n)]= runSR(n,V,experiment,T)
    
    print(time.time() - start_time)    
    return result
             
"""
Runs the experiment T times and returns error e_n
"""
def runSR(n,V,experiment,T):
    error = 0.0
    for t in range(T):
        value = SR(n,V,experiment)
        error = error + value
        
    return error/float(T)

"""
Function that runs the main SAR algorithm, input parameters are:
n - number of rounds
V - number of vertices in complete graph
experiment - experiment # to run the simulation on (predefined in paper)
"""
def SR(n,V,experiment): 
    # arms = number of edges in complete graph with vertices V
    K = (V*(V-1))/2 
    
    A=list(xrange(0,K)) # active arms set (Indexed from 0 to K-1)
    actual_means=oracle_means(experiment)
    
    rewards=[0]*K # sum of the rewards of each arm that has been sampled
    rounds=[0]*K # count of total number rounds each arm has been sampled
    empirical_means=[0]*K # set of the empirical means of arms
    
    acceptedset=[] # list of the accepted edges
    oracleset=oracle_set(experiment)
            
    phase=list(xrange(1,K)) # set of phases
    
    # main for-loop over the phases

    for alpha in phase:
                                                
        # number of samples of each active arm
        numberRounds=rounds_SAR(n,K,alpha)-rounds_SAR(n,K,alpha-1)
        
        # for each active arm in A
        for active in A:
            arm_samples = bernoulli.rvs(actual_means[active],size=numberRounds)
            rewards[active]=rewards[active]+sum(arm_samples)
            rounds[active]=rounds[active]+numberRounds
            empirical_means[active]=(rewards[active]/float(rounds[active]))
        
        # Find the lowest empirical mean among Active arms
        tempmeans=[0]*len(A)
        for arm in A:
            tempmeans[A.index(arm)]=empirical_means[arm]
        dic1 = dict(zip(A,tempmeans))
        idx=min(dic1,key=dic1.get)
        
        # Stop sampling that arm
        A.remove(idx)
 
    acceptedset = calcMaxST(V,empirical_means) # Indices of ARMS of MaxST
    
    print('final_acceptedset: ' + str(acceptedset))   
    if set(acceptedset)==set(oracleset):
        return 1.0
    else:
        return 0.0