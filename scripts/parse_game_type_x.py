#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parsing of a csv game tracking sheet of type 'X', saving data in consice and relevant manner."""

# Here comes your imports
import sys
import pandas as pd

# Here comes your (few) global variables

# Here comes your class definitions

# Here comes your function definitions

def parse_shot_result(data):
    """parse the result of the event / shot"""
    result_categories = ['BL', 'MI', 'SOG', 'G']
    shot_results = data[result_categories]
    print(shot_results.info())
    result_count = shot_results.notna().sum(axis=1)
    print('no shot result:\n', shot_results[result_count < 1])
    print('multiple shot results:\n', shot_results[result_count > 1])
    result = pd.Categorical([''] * len(shot_results.index), categories=result_categories)
    for label, content in shot_results.items():
        result[content.notna()] = label
    print(pd.Series(result))
    print(pd.Series(result).value_counts())

def parse_involved_players_for(data):
    """parse the involved (on-field) players for"""
    prefix = 'hm_'
    players_goalies = data.filter(regex=("^g?[0-9]+$"))
    numbers = pd.Series(list(players_goalies))
    col = [prefix + str(i) for i in range(1, 7)]
    players = pd.DataFrame('', index=players_goalies.index, columns=col)
    for index, event in players_goalies.iterrows():
        players_on = numbers[event.notna().values]
        player_count = len(players_on)
        if len(col) >= player_count:
            players.iloc[index, 0:player_count] = players_on.values
        else:
            print('too many players, index : ', index)
            print(players_on)
    print(players)

def parse_involved_players_against(data):
    """parse the involved (on-field) players against"""
    prefix = 'aw_'
    suffix = '_against'
    players_goalies = data[['players' + suffix, 'goalie' + suffix]]
    default_number = '?'
    col = [prefix + str(i) for i in range(1, 7)]
    players = pd.DataFrame('', index=players_goalies.index, columns=col)
    for index, event in players_goalies.iterrows():
        players_on = \
            ([default_number] * event.loc['players' + suffix]) + \
            (['g' + default_number] * event.loc['goalie' + suffix])
        player_count = len(players_on)
        if len(col) >= player_count:
            players.iloc[index, 0:player_count] = players_on
        else:
            print('too many players, index : ', index)
            print(players_on)
    print(players)

def parse_acting_players(data):
    """parse the acting players (shot, assist, block) from the columns with player numbers"""
    players_goalies = data.filter(regex=("^g?[0-9]+$"))
    actions = pd.DataFrame('', index=players_goalies.index, columns=['shot', 'assist', 'block'])
    for col in players_goalies:
        player = players_goalies[col].astype(str)
        nbr = col.replace('g', '')
        actions['shot'][player.str.match('S')] = nbr
        actions['assist'][player.str.match('A')] = nbr
        actions['block'][player.str.match('B')] = nbr
    print(actions)
    print(actions.info())

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
    filename = 'x'
    datafile = datadir + filename + '.csv'
    print(datafile)

    data = pd.read_csv(datafile, quotechar="'")
    print(data)

#    parse_time(data)
#    parse_period(data)
#    parse_team(data)
#    parse_acting_players(data)
#    parse_involved_players_for(data)
#    parse_involved_players_against(data)
#    parse_shot_result(data)

#    data.to_pickle(datadir + filename + '.pkl.xz')

if __name__ == "__main__":
    main()
