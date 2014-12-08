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

"""
draw_graph
    Plots the networkx graph from a file with the edge transparency varying by
    the transmission rate for each edge.
"""
def draw_graph(fname, network_file, title, pos=None):
    G = nx.read_edgelist(fname, delimiter=' ',nodetype=int,
            data=(('weight',float),),create_using=nx.Graph())

    node_lst = []
    label_dict = {}
    with open(network_file) as f:
        for line in f:
            if len(line) <= 1:
                continue
            (int_val, label) = line.split(',')
            label = label[:-1]
            node_lst.append(label)
            label_dict[int(int_val)] = label

    labelled_G = nx.Graph()
    labelled_G.add_nodes_from(node_lst)

    if '8\r' in labelled_G.nodes():
        labelled_G.remove_node('8\r')

    for src, dest in G.edges():
        if src not in label_dict or dest not in label_dict:
            print src, dest
            continue
        labelled_G.add_edge(label_dict[src], label_dict[dest],
                weight = G[src][dest]['weight'])

    if pos == None:
        pos = nx.circular_layout(labelled_G)

    nx.draw_networkx_nodes(labelled_G, pos,
            node_color='#ADD8E6', node_size=100, alpha=0.8)
    # nx.draw_networkx_labels(labelled_G, pos, font_size=7)

    """
    if 'inferred' in fname:
        nx.draw_networkx_edges(labelled_G, pos,
            width = 1,
            edge_color = 'black'
            )
    else:
    """
    if 'inferred' in fname:
        threshold_val = 0.163
    else:
        threshold_val = 2.88
    edge_lst = [x for x in labelled_G.edges() if
                labelled_G[x[0]][x[1]]['weight'] > threshold_val]

    if True:
        nx.draw_networkx_edges(labelled_G, pos,
            edgelist = edge_lst,
            # edge_color=[labelled_G[x[0]][x[1]]['weight'] for x in edge_lst],
            # edge_cmap=plt.cm.Greys,
            width = 1,
            edge_vmin = -5,
            edge_vmax = 14,
            edge_color = 'black',
            alpha=0.8
        )

    plt.title(title + ' Ebola Network')
    plt.show()

    return pos

def plot_tb_networks():
    pos = draw_graph('tb_data/tb_updated_avg.txt', 'tb_data/tb-network.txt',
            'Updated')
    draw_graph('tb_data/tb_inferred_avg.txt', 'tb_data/tb-network.txt',
            'InfoPath Inferred', pos)
    draw_graph('tb_data/tb-truth-newlabel.txt', 'tb_data/tb-network.txt',
            'Ground-Truth', pos)

def plot_ebola_networks():
    pos = draw_graph('ebola_data/ebola_updated_avg.txt',
            'ebola_data/node_ids.txt',
            'Updated')
    draw_graph('ebola_data/ebola_inferred_avg.txt',
            'ebola_data/node_ids.txt',
            'InfoPath Inferred', pos)

plot_ebola_networks()

