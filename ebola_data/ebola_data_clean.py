"""
ebola_data_clean.py

File to take the strings from the Ebola network and convert into timestamps.
"""

import csv
import datetime
import pandas as pd
import re


"""
str_to_date
    Function that takes the long string form describing an infection point and
    takes only the substring with the date of infection.

"""
def str_to_date(df):
    regex_str = '2014-.*'

    date_arr = []

    min_date = datetime.datetime.today()

    for index, row in df.iterrows():
        s = row['ebola_id']
        m = re.search(regex_str, s)

        date_str = m.group(0)
        date_val = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        date_arr.append(date_val)

        if date_val < min_date:
            min_date = date_val

    df['date'] = date_arr

    return min_date


"""
date_to_step
    Function that takes columns of dates (yyyy-mm-dd) and converts them into
    timesteps on the order of days, where t=0 on the earliest day in the column.

"""
def date_to_step(df, min_date):
    t_arr = []

    for index, row in df.iterrows():
        date = row['date']

        diff = date - min_date
        t_arr.append(diff.days)

    df['timestep'] = t_arr


"""
df_to_txt
    Function to convert the dataframe of timesteps to cascades and network data
    files necessary as input to the InfoPath algorithm.

"""
def df_to_txt(df, network_name):
    outcsv = csv.writer(open(network_name + '_cascades.txt', 'w+'), delimiter=';',
            quoting = csv.QUOTE_NONE)

    for key in xrange(1, 5):
        # cascade_id, cascade_name (same)
        key_str = str(key)
        outcsv.writerow([key_str + ',' + key_str])

    outcsv.writerow([])

    grouped_df = df.groupby('clade')

    for clade, group in grouped_df:
        lst_str = ''
        for index, row in group.iterrows():
            lst_str = lst_str + ',' + str(index) + ',' + str(row['timestep'])

        outcsv.writerow([clade, lst_str[1:]])


    # writing the network to a file as well
    outcsv = csv.writer(open(network_name + '_network.txt', 'w+'), quoting =
            csv.QUOTE_NONE)

    for i in df.index:
        outcsv.writerow([i, i])


def main():
    df = pd.read_csv('ebola_data.csv')

    min_date = str_to_date(df)
    date_to_step(df, min_date)

    df.to_csv('ebola_cleaned.csv', index=False)

    df_to_txt(df, 'ebola')


if __name__ == "__main__":
    main()
