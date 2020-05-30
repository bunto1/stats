#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parsing of a csv game tracking sheet of type 'X', saving data in consice and relevant manner."""

# Here comes your imports
import sys
import pandas as pd

# Here comes your (few) global variables

# Here comes your class definitions

# Here comes your function definitions

def parse_team(data):
    """parse the team (home/away) from two columns"""
    home_name = 'x'
    away_name = 'y'
    home_away = data[[home_name, away_name]]
    print(home_away.info())
    print(home_away.isnull().sum().sum() == len(home_away.index))
    team = pd.Series([''] * len(home_away.index))
    team[home_away[home_name].isnull()] = 'away'
    team[home_away[away_name].isnull()] = 'home'
    print(team)

def parse_period(data):
    """parse the period int-string into int (OT => 4)"""
    period = data['period']
    period.replace('OT', '4', inplace=True)
    print(period.astype(int))

def parse_time(data):
    """parse video time float-string into minutes and seconds"""
    time_as_str = data['time_vid'].astype(str)
    vd_m_s = time_as_str.str.split('.', expand=True)
    vd_m_s.set_axis(['vd_m', 'vd_s'], axis=1, inplace=True)
    print(vd_m_s)

    gm_m = data['time_game_m']
    print(gm_m)
    gm_m_nan = gm_m.head.isnull()
    print(gm_m_nan)
#    blocks = (gm_m_nan.shift(1) != gm_m_nan).astype(int).cumsum()
#    inds = pd.Series(gm_m_nan.index[gm_m_nan])

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

#    parse_time(data)
#    parse_period(data)
#    parse_team(data)

#    data.to_pickle(datadir + filename + '.pkl.xz')

if __name__ == "__main__":
    main()
