"""
Created on Mar 23, 2013

Script to run Uniform Sampling to find a Maximum Weighted Spanning Tree on a complete graph.
NOTE: THERE IS A DISJOINT IN HOW EDGES ARE ASSIGNED TO GRAPH CURRENTLY DONE TOO SIMPLISTICALLY! - ngurnani on 03/28/13

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
from MaxST_sidefunctions import *

"""
Quick and Dirty function to compute values (need to implement proper dataframe structure later)
"""
def quickSolUni(V,experiment,T,n_index):
    start_time = time.time()        
    #n_index = range(100,10001,100)
    result = [0]*len(n_index)
    for n in n_index:
        result[n_index.index(n)]= runUni(n,V,experiment,T)
    
    print(time.time() - start_time)
    
    return result
    
"""
Runs the experiment T times and returns error e_n
"""
def runUni(n,V,experiment,T):
    start_time = time.time()
    error = 0.0
    for t in range(T):
        value = SAR(n,V,experiment)
        error = error + value
    
    print(time.time() - start_time)    
    return (error/float(T))

"""
Function that runs the main SAR algorithm, input parameters are:
n - number of rounds
V - number of vertices in complete graph
experiment - experiment # to run the simulation on (predefined in paper)
"""
def SAR(n,V,experiment): 
    # arms = number of edges in complete graph with vertices V
    K = (V*(V-1))/2 
    
    actual_means=oracle_means(experiment)
    oracleset=oracle_set(experiment)
    
    rewards=[0]*K # sum of the rewards of each arm that has been sampled
    rounds=[0]*K # count of total number rounds each arm has been sampled
    empirical_means=[0]*K # set of the empirical means of arms
    
    # Sample each arm n/K times
    numbersamples= floor(n/K) # inherently floored because diving two integers
    
    for arm in range(K):
        arm_samples = bernoulli.rvs(actual_means[arm],size=numbersamples)
        rewards[arm]=rewards[arm]+sum(arm_samples)
        rounds[arm]=rounds[arm]+numbersamples
        empirical_means[arm]=(rewards[arm]/float(rounds[arm]))
        
    acceptedset = calcMaxST(V,empirical_means) # Indices of ARMS of MaxST
    
    if set(acceptedset)==set(oracleset):
        return 1.0
    else:
        return 0.0