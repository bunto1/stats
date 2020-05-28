#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parsing of a csv game tracking sheet of type 'X', saving data in consice and relevant manner."""

# Here comes your imports
import sys
import pandas as pd

# Here comes your (few) global variables

# Here comes your class definitions

# Here comes your function definitions

def parse_time(data):
    """parse video time float-string into minutes and seconds"""
    time_as_str = data['time_vid'].astype(str)
    vid_m_s = time_as_str.str.split('.', expand=True)
    vid_m_s.set_axis(['vd_m', 'vd_s'], axis=1, inplace=True)
    print(vid_m_s)

def main():
    """Launcher."""
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    datadir = 'data/'
    filename = 'R01'
    datafile = datadir + filename + '.csv'
    print(datafile)

    data = pd.read_csv(datafile, quotechar="'")
    print(data)

    parse_time(data)

    data.to_pickle(datadir + filename + '.pkl.xz')

if __name__ == "__main__":
    main()
