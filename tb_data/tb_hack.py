"""
tb_hack.py

"""
import csv

bad_dict = {}

with open('tb-truth.txt') as f:
    for line in f:
        if line == '\n':
            break
        (int_val, label) = line.split(',')
        label = label[:-1]
        bad_dict[int_val] = label


outcsv = csv.writer(open('tb-truth-newlabel.txt', 'w+'), delimiter=' ',
        quoting = csv.QUOTE_NONE)

with open('tb-truth_avg.txt') as f:
    for line in f:
        if line == '\n':
            break
        (src, dest, weight) = line.split(' ')
        weight = weight[:-1]

        new_src = int(bad_dict[src][2:]) - 1
        new_dest = int(bad_dict[dest][2:]) - 1

        outcsv.writerow([new_src, new_dest, weight])


