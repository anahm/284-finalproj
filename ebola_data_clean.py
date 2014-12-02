"""
ebola_data_clean.py

File to take the strings from the Ebola network and convert into timestamps.
"""

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


def main():
    df = pd.read_csv('ebola_data.csv')

    min_date = str_to_date(df)
    date_to_step(df, min_date)

    df.to_csv('ebola_data_output.csv', index=False)


if __name__ == "__main__":
    main()
