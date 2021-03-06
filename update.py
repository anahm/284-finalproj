"""
update.py
Takes in weighted network file produced by InfoPath, returns network
 with updated transmission rate distributions.
"""

from scipy import stats
import numpy as np

import csv
import matplotlib.pyplot as plt
import networkx as nx
import random
import itertools

"""
load_infopath
    Function to load network generated by InfoPath.
    @param: file name
    @ret: weighted Networkx graph
"""
def load_infopath(fname):
    # Load infopath output lines
    f = open(fname, 'rU')
    lines = [l for l in f]

    # Break lines into the node names and the edge attributes
    split = lines.index('\n')

    # Generate graph
    G = nx.DiGraph()
    node_names=[int(l.split(',')[0]) for l in lines[:split]]
    G.add_nodes_from(node_names)

    # Clean up edges
    edges_raw = [l.split(',') for l in lines[split+1:]]
#    edges_clean = [((int(l[0]),int(l[1])), np.mean(map(float, l[3::2]))) for l in edges_raw]
    edges_clean = [((int(l[0]),int(l[1])), float(l[-1])) for l in edges_raw]
    # Add edges to graph
    for e in edges_clean:
        if e[1]>0:
            G.add_edge(e[0][0],e[0][1], weight=e[1])
    nx.write_weighted_edgelist(G, fname[:-4]+'_avg.txt')

    return G


"""
load_prior
    Function to load network with transmission priors.
    @param: file name
    @ret: weighted Networkx graph
"""
def load_prior(fname):
    # Gamma parameters
    alpha = 1.
    beta = 2.
    
    # Load graph
    G = nx.read_edgelist(fname, delimiter=',',nodetype=int, data=(('weight',float),),create_using=nx.DiGraph())

    # New graph to add priors to
    R = nx.complete_graph(len(G.nodes()),create_using=nx.DiGraph())
    # If e was in the original graph, use its prior. Else give it a (0,0) prior.
    for e in R.edges():
        if e in G.edges():
            R[e[0]][e[1]]['params'] = (alpha,beta)
        elif e not in G.edges():
            R.add_edge(e[0],e[1],attr_dict={'params':(0.,0.)})
    return R

"""
update
    Updates prior network with InfoPath estimates.
    @param: infopath file name, prior file name
    @ret: weighted Networkx graph
"""
def update(infoname, priorname):
    # Load graphs
    U = load_infopath(infoname)
    P = load_prior(priorname)
    
    to_remove = []
    # If InfoPath has an estimate for an edge, update it
    for e in P.edges():
        if e in U.edges():
            P[e[0]][e[1]]['params'] = (P[e[0]][e[1]]['params'][0]+1, P[e[0]][e[1]]['params'][1]+1./U[e[0]][e[1]]['weight'])
        if P[e[0]][e[1]]['params'] == (0,0):
            to_remove.append(e)
    P.remove_edges_from(to_remove)
    return P


def main():
    infoname = 'sim_data_inferred.txt'
    priorname = 'sim_data_prior.txt'
    outname = 'updated.txt'
    outavgname = 'updated_avg.txt'
    
    G = update(infoname, priorname)
    for e in G.edges():
        print G[e[0]][e[1]]['params']
        print e, stats.gamma(G[e[0]][e[1]]['params'][0], scale=1./G[e[0]][e[1]]['params'][1]).stats(moments='m')
    nx.write_edgelist(G,outname)
    A = G.copy()
    for e in A.edges():
        p = stats.gamma(G[e[0]][e[1]]['params'][0], scale=1./G[e[0]][e[1]]['params'][1]).stats(moments='m')
#       if p == nan: A[e[0]][e[1]]['weight'] = 0
        A[e[0]][e[1]]['weight'] = p
    nx.write_weighted_edgelist(A,outavgname,delimiter=',')

if __name__ =='__main__':
    main()