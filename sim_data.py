"""
sim_data.py

File with functions related to creating/analyzing simulated network data to be
used for the overall network inference algorithm.

"""

from scipy import stats

import csv
import matplotlib.pyplot as plt
import networkx as nx
import os
import random


"""
make_network
    Function that creates a random directed graph and assigns transmission rates
    to each edge based on a gamma distribution.

    @param: a, b - parameters for gamma distribution
    @ret: networkx graph G with transmission rates in 'trans_rate' attribute
"""
def make_network(num_nodes, prob_edge_creation, a, b):
    # create graph
    # XXX see link below for addl random graphs
    # http://networkx.lanl.gov/reference/generators.html#module-networkx.generators.random_graphs
    G = nx.erdos_renyi_graph(num_nodes, prob_edge_creation, directed=True)

    # assign transmission values per edge
    for src,dest in G.edges():
        trans_rate = stats.gamma.rvs(a, b)
        G[src][dest]['trans_rate'] = trans_rate

    return G


"""
make_cascade
    Function to simulate a cascade traversing a network.

    @param: networkx graph G with transmission rates as weights
    @ret: list of tuples (node_id, infection_time) that has at least one element
"""
def make_cascade(G, max_time, show_vis):
    time_step = 0

    # initialization with randomly selected source node
    src = random.choice(G.nodes())
    infection_dict = {}
    infection_dict[src] = time_step

    # for vis-test purposes
    cascade_edges = []

    # XXX is there a better way to cut off the cascade creation process?
    while time_step < max_time:
        time_step += 1

        # assuming any node can infect any neighboring node
        for node in infection_dict.keys():
            for n in G.neighbors(node):
                if n in infection_dict:
                    # already infected
                    continue

                # scale = 1/lambda
                trans_rate = G[node][n]['trans_rate']
                prob_infection = stats.expon.cdf(time_step,
                        scale=1.0 / trans_rate)

                if stats.uniform.rvs(0, 1) <= prob_infection:
                    # infected!
                    infection_dict[n] = time_step
                    cascade_edges.append((node, n))

    if show_vis:
        node_color = ['red' if node == src else '#ADD8E6' for node in G.nodes()]
        edge_color = ['red' if edge in cascade_edges else 'black' for edge in
                G.edges()]
        print_graph(G, node_color, edge_color)

    return infection_dict.items()


"""
cascades_to_file
    Function to write the cascades to the proper InfoPath input format.

    @param: outfile name, dictionary (cascade_id --> infection_lst)
"""
def cascades_to_file(outfile_name, cascade_dict):
    outcsv = csv.writer(open(outfile_name, 'w+'), delimiter=';',
            quoting = csv.QUOTE_NONE)

    # print
    for key in cascade_dict.keys():
        # cascade_id, cascade_name (same)
        key_str = str(key)
        outcsv.writerow([key_str + ',' + key_str])

    outcsv.writerow([])

    for key, lst in cascade_dict.iteritems():
        lst_str = ",".join("%d,%d" % tup for tup in lst)
        print lst

        # lst_str = str(lst).strip('[]')
        outcsv.writerow([key, lst_str])


"""
network_to_file
    Function to write the nodes of the network to the proper Infopath input
    format.

    @param: outfile name, networkx graph G
"""
def network_to_file(network_file, truth_file, G):
    outcsv = csv.writer(open(network_file, 'w+'), delimiter=',')

    # print
    for node in G.nodes():
        # node_id, node_name (same)
        outcsv.writerow([node, node])

    # also printing true network
    outcsv = csv.writer(open(truth_file, 'w+'), delimiter=',')

    for src, dest in G.edges():
        outcsv.writerow([src, dest, G[src][dest]['trans_rate']])


"""
write_files
    Function to write all of the necessary files into a directory.

    @param: network_name, cascade_dict (cascade_id -> lst), graph G
"""
def write_files(network_name, cascade_dict, G):
    if not os.path.exists(network_name):
        os.makedirs(network_name)

    network_name = network_name + '/' + network_name
    # XXX write out parameter info to a readme
    readme = open(network_name + '_readme.txt', 'w+')
    readme.write(network_name)

    cascades_to_file(network_name + '_cascades.txt', cascade_dict)
    network_to_file(network_name + '_network.txt', network_name + '_truth.txt', G)


"""
make_infopath_input
    Function to create the proper file input for the InfoPath algorithm with a
    simulated dataset.

    @param: show_vis - boolean to show graphs depicting the network (only works
    for small graphs!)
    @ret: n/a
"""
def make_infopath_input(show_vis=False):
    # variables
    num_nodes = 10
    prob_edge_creation = 0.5
    alpha_param = 0.5
    beta_param = 0.5
    num_cascades = 10
    cascade_max_time = 10
    network_name = 'sim_data'

    # make_network
    G = make_network(num_nodes, prob_edge_creation, alpha_param, beta_param)

    if show_vis:
        # show regular graph
        print_graph(G, '#ADD8E6', 'black')

    # convert to infopath file input
    cascade_dict = {}

    # given this network, create a cascade
    for i in xrange(num_cascades):
        infection_lst = make_cascade(G, cascade_max_time, show_vis)
        cascade_dict[i] = infection_lst

    write_files(network_name, cascade_dict, G)

    print 'Saved To: ' + network_name


"""
print_graph
    Function to print the graph.

    @param: graph G, node_color, edge_color
"""
def print_graph(G, node_color, edge_color):
    edge_labels=dict([((u,v,),int(d['trans_rate']))
                 for u,v,d in G.edges(data=True)])
    pos=nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    nx.draw_networkx(G, pos, with_labels=True,
            # width=[G[a][b]['trans_rate'] for a,b in G.edges()],
            node_color=node_color, edge_color=edge_color)
    plt.show()


def main():
    # where the magic begins...
    make_infopath_input(show_vis=True)


if __name__ == "__main__":
    main()
