"""
sim_data.py

File with functions related to creating/analyzing simulated network data to be
used for the overall network inference algorithm.

"""

import networkx as nx
import stats from scipy


"""
make_network
    Function that creates a random directed graph and assigns transmission rates
    to each edge based on a gamma distribution.

    @param: a, b - parameters for gamma distribution
    @ret: networkx graph G with transmission rates in 'trans_rate' attribute
"""
def make_network(a, b):
    # create graph
    # XXX see link below for addl random graphs
    # http://networkx.lanl.gov/reference/generators.html#module-networkx.generators.random_graphs
    num_nodes = 10
    prob_edge_creation = 0.5
    G = nx.erdos_renyi_graph(num_nodes, prob_edge_creation, directed=True)

    # assign transmission values per edge
    for src,dest in G.edges():
        # XXX does this need to be a value between 0 and 1?
        trans_rate = stats.gamma.rvs(a, b)
        G[src][dest]['trans_rate'] = trans_rate

    return G


"""
make_cascade
    Function to simulate a cascade traversing a network.

    @param: networkx graph G with transmission rates as weights
    @ret: list of tuples (node_id, infection_time) that has at least one element
"""
def make_cascade(G):
    # randomly select source node
    src = 

    infection_lst = [(src, 0)]
    to_visit = [src]
    time_step = 1

    while len(to_visit) > 0:
        for node in to_visit:
            for n in G.neighbors(node):
                # scale = 1/lambda
                trans_rate = n['trans_rate']
                print trans_rate
                prob_infection = stats.expon.cdf(time_step,
                        scale=1.0 / trans_rate)



    pass


"""
cascades_to_file
    Function to write the cascades to the proper InfoPath input format.

    @param: outfile name, dictionary (cascade_id --> infection_lst)
"""
def cascades_to_file(outfile_name, cascade_dict):
    """
    outfile = open(outfile_name, w+)

    # print
    for key in cascade_dict.keys():
        # cascade_id, cascade_name (same)
        writeline([key, key])

    for key, lst in cascade_dict.iteritems():
        lst_str = str(lst)[1:-1]
        writeline([key, lst_str])
    """



"""
make_infopath_input
    Function to create the proper file input for the InfoPath algorithm with a
    simulated dataset.

    @param: n/a
    @ret: n/a
"""
def make_infopath_input():
    # make_network
    alpha = 2
    beta = 2
    G = make_network(alpha, beta)

    # convert to infopath file input
    cascade_dict = {}

    num_cascades = 5
    # given this network, create a cascade
    for i in xrange(num_cascades):
        infection_lst = make_cascade(G)
        cascade_dict[i] = infection_lst


    print 'Saved To: ' + 'outfile name'
    pass



