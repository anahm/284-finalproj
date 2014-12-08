"""
real_data.py

Runs analysis on real datasets.
"""

from utils import *
from update import *

def compute_mae(inferred_file, updated_file, truth_file, priors_file, nodes_file):
    node_names = nodes(nodes_file)

    # mae for infopath
    inferred = load_infopath(inferred_file)
    inf_lst = [(e[0], e[1], inferred[e[0]][e[1]]['weight']) for e in
            inferred.edges()]

    truth = load_infopath(truth_file)
    truth_lst = [(e[0], e[1], truth[e[0]][e[1]]['weight']) for e in
            truth.edges()]


    infopath_mae = mae(inf_lst, truth_lst, node_names)
    print 'InfoPath MAE: ' + str(infopath_mae)

    """
    # mae for new algo
    updated_lst = np.genfromtxt(outavgname, delimiter=',')

    algo_mae = mae(updated_lst, truth_lst, node_names)
    print 'Algo MAE: ' + str(algo_mae)
    """

    # mae for prior net
    prior_lst = np.genfromtxt(priors_file, delimiter=' ')
    prior_mae = mae(prior_lst,truth_lst,node_names)
    print 'Prior MAE: ' + str(prior_mae)


nodes_file = 'tb_data/tb-network.txt'
truth_file = 'tb_data/tb-truth.txt'
priors_file = 'tb_data/prior_edgelist_tb.txt'

inferred_file = 'tb_data/tb_inferred.txt'
updated_file = 'tb_data/tb-updated.txt'
compute_mae(inferred_file, updated_file, truth_file, priors_file, nodes_file)


"""
nodes_file = 'sars_data/sars-network.txt'
truth_file = 'sars_data/sars-truth.txt'

inferred_file = 'sars_data/sars-inferred.txt'
updated_file = 'sars_data/sars-updated.txt'
compute_mae(inferred_file, updated_file, truth_file, nodes_file)
"""
