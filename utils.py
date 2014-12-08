"""
utils.py

Useful functions for network recovery/inference.

"""

from scipy import stats
import numpy as np

import csv
import matplotlib.pyplot as plt
import networkx as nx
import random
import itertools
from collections import defaultdict

"""
nodes
    Function to get graph nodes from InfoPath input.

    @param: file name
    @ret: list of nodes
"""
def nodes(fname):
    # Load infopath output lines
    f = open(fname, 'rU')
    lines = [l for l in f]

    # Break lines into the node names and the edge attributes
    split = lines.index('\n')

    # Generate graph
    G = nx.DiGraph()
    node_names=[int(l.split(',')[0]) for l in lines[:split]]
    return node_names

"""
mae
    Function to calculate mean abs error.

    @param: recovered network, true network as edgelists of [u,v,weight]
    @ret: MAE value
"""
def mae(estimate, truth, node_names):
	td = defaultdict(int)
	td.update({(r[0],r[1]):r[2] for r in truth})
	ed = defaultdict(int)
	ed.update({(r[0],r[1]):r[2] for r in estimate})
	return np.mean([np.abs(td[k]-ed[k]) for k in itertools.product(node_names,node_names)])

"""
pair_dist
    Calculates pairwise (Hamming) distances between genetic sequences.

    @param: numpy array of sequences
    @ret: pairwise distance matrix
"""
def pair_dist(seqarray):
    pd = np.zeros((seqarray.shape[0],seqarray.shape[0]))
    for i,j in itertools.product(xrange(seqarray.shape[0]),xrange(seqarray.shape[0])):
        pd[i,j] = np.sum(seqarray[i]!=seqarray[j])
    return pd
