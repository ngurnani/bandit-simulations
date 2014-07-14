"""
Created on Mar 19, 2013

Script for the SAR Algorithm to find a Maximum Weighted Spanning Tree on a complete graph.
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
import operator 
from scipy.stats import bernoulli
from MaxST_sidefunctions import *

"""
Quick and Dirty function to compute values (need to implement proper dataframe structure later)
"""
def quickSolSAR(V,experiment,T,n_index):
    start_time = time.time()        
    #n_index = range(100,10001,100)
    result = [0]*len(n_index)
    for n in n_index:
        result[n_index.index(n)]= runSAR(n,V,experiment,T)
    
    print(time.time() - start_time)    
    return result
             
"""
Runs the experiment T times and returns error e_n
"""
def runSAR(n,V,experiment,T):
    error = 0.0
    for t in range(T):
        value = SAR(n,V,experiment)
        error = error + value
        
    return error/float(T)

"""
Function that runs the main SAR algorithm, input parameters are:
n - number of rounds
V - number of vertices in complete graph
experiment - experiment # to run the simulation on (predefined in paper)
"""
def SAR(n,V,experiment): 
    # arms = number of edges in complete graph with vertices V
    K = (V*(V-1))/2 
    
    m=V-1 # size of maximum matching
    A=list(xrange(0,K)) # active arms set (Indexed from 0 to K-1)
    actual_means=oracle_means(experiment)
    
    rewards=[0]*K # sum of the rewards of each arm that has been sampled
    rounds=[0]*K # count of total number rounds each arm has been sampled
    empirical_means=[0]*K # set of the empirical means of arms
    
    acceptedset=[] # list of the accepted edges
    oracleset=oracle_set(experiment)
    
    allarms = list(xrange(0,K))
    [allarms.remove(j) for j in oracleset]
        
    phase=list(xrange(1,K)) # set of phases
    
    # main for-loop over the phases

    for alpha in phase:
        #print('ALPHA: ' + str(alpha))
        #print('A: ' + str(A))
        
        ####################################################################
        # POSSIBLE ERROR 1 - Accept an incorrect arm
        shortcircuit=set(allarms).intersection(set(acceptedset))
        if shortcircuit:
            print('shortCircuit: ' + str(shortcircuit))
            return 0.0
            
        templst=list()
        for arm in oracleset:
            if arm not in A:
                templst.append(arm)
        for arm in templst:
            if arm not in acceptedset:
                return 0.0
        
        # if you've selected all the necessary arms don't need to run anymore phases?
        if m==0 and set(acceptedset)==set(oracleset):
            return 1.0
        elif m==0:
            return 0.0
        ####################################################################

                                                
        # number of samples of each active arm
        numberRounds=rounds_SAR(n,K,alpha)-rounds_SAR(n,K,alpha-1)
        
        # for each active arm in A
        for active in A:
            arm_samples = bernoulli.rvs(actual_means[active],size=numberRounds)
            rewards[active]=rewards[active]+sum(arm_samples)
            rounds[active]=rounds[active]+numberRounds
            empirical_means[active]=(rewards[active]/float(rounds[active]))
        
        # 2.
        sample_T = calcMaxST(V,empirical_means) # Indices of ARMS of MaxST
        
        # 3.
        ordered = orderT_Arm(sample_T, empirical_means)
        ordered_T = [arm for arm in ordered if arm in A] # removes arms not in A

        # TEST
        ####################################################################
        empirical_gaps=empiricalgaps(m,A,ordered_T,empirical_means)

        # KIND OF DICTIONARY SOLUTION TO BUG ISSUE <--- Built in Bias if bug is max[0.0,0.0] always returns 0
        temp=[0]*len(A)
        for arm in A:
            temp[A.index(arm)]=empirical_gaps[arm]
        dic1 = dict(zip(A,temp))
        max_idx=max(dic1,key=dic1.get)

        #print('m: ' + str(m))
        #print('empirical_means: ' + str(empirical_means))
        #print('rewards: ' + str(rewards))
        #print('rounds: ' + str(rounds))
        #print('ordered_T: ' + str(ordered_T))
        #print('empirical_gaps: ' + str(empirical_gaps))
        #print('max_idx: ' + str(max_idx))
        #print('beforeChange_acceptedset: ' + str(acceptedset))

        ####################################################################
                
        if empirical_means[max_idx] >= empirical_means[ordered_T[m]]:
            acceptedset.append(max_idx)
            m=m-1
        
        #print('afterChange_acceptedset: ' + str(acceptedset))

        A.remove(max_idx)
        empirical_means[max_idx]=-2
        rewards[max_idx]=-2
        rounds[max_idx]=-2
 
    print('final_acceptedset: ' + str(acceptedset))   
    if set(acceptedset)==set(oracleset):
        return 1.0
    else:
        return 0.0
        
def empiricalgaps(m,A,ordered_T,empirical_means):
    gap=[0]*len(empirical_means)
    for arm in A:
        #print('mainArm: ' + str(arm))
        #print('gap: ' + str(gap))
        if (arm) in ordered_T[0:m]:
            #print('IF_arm: ' + str(arm))
            #print('IF_em: ' + str(empirical_means))
            #print('IF_m: ' + str(m))
            #print('IF_orderedT: ' + str(ordered_T))
            
            gap[arm] = abs(empirical_means[arm] - empirical_means[ordered_T[m]])
        elif (arm) in ordered_T[m:]:
            gap[arm] = abs(empirical_means[ordered_T[m-1]]- empirical_means[arm])
    
    return gap    