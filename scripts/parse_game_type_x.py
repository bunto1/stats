#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parsing of a csv game tracking sheet of type 'X', saving data in consice and relevant manner."""

# Here comes your imports
import sys
import logging as log
import pandas as pd

# Here comes your (few) global variables

# Here comes your class definitions

# Here comes your function definitions
def parse_pre_shot_situation(data, out):
    """parse the situation leading to the shot"""
    # (cycle / free-hit / develop / counter / turnover / rebound / penalty / others)
    situation_labels = \
        ['Festsetzen', 'Freischlag', 'Auslösung', 'Konter', \
         'Ballgewinn', 'Abpraller', 'Penalty', 'Sonstige']
    situation_categories = \
        ['CYC', 'FHT', 'DVL', 'CNT', 'TNV', 'RBD', 'PNT', 'OTH']
    shot_situations = data[situation_labels]
    shot_situations.columns = situation_categories
    situation_count = shot_situations.notna().sum(axis=1)
    if (situation_count != 1).any():
        log.warning('no pre shot situation:\n%s', shot_situations[situation_count < 1])
        log.warning('multiple pre shot situations:\n%s', shot_situations[situation_count > 1])
    situation = pd.Categorical([''] * len(shot_situations.index), categories=situation_categories)
    for label, content in shot_situations.items():
        situation[content.notna()] = label
    log.debug(pd.Series(situation))
    log.debug(pd.Series(situation).value_counts())
    out['sh_situ'] = pd.Series(situation)

def parse_shot_type(data, out):
    """parse the type of the shot"""
    # (wrist / chip / slap / backhand / one-timer / volley / tip / in-tight)
    type_labels = \
        ['Gezogen', 'Chip', 'Slapshot', 'Backhand', 'Direkt', 'Volley', 'Ablenker', 'InTight']
    type_categories = \
        ['WRS', 'CHP', 'SLP', 'BKH', 'ONT', 'VOL', 'TIP', 'INT']
    shot_types = data[type_labels]
    shot_types.columns = type_categories
    type_count = shot_types.notna().sum(axis=1)
    if (type_count != 1).any():
        log.warning('no shot type:\n%s', shot_types[type_count < 1])
        log.warning('multiple shot types:\n%s', shot_types[type_count > 1])
    shot_type = pd.Categorical([''] * len(shot_types.index), categories=type_categories)
    for label, content in shot_types.items():
        shot_type[content.notna()] = label
    log.debug(pd.Series(shot_type))
    log.debug(pd.Series(shot_type).value_counts())
    out['sh_type'] = pd.Series(shot_type)

def parse_shot_result(data, out):
    """parse the result (blocked / missed / on-goal / goal) of the event / shot"""
    result_categories = ['BL', 'MI', 'SOG', 'G']
    shot_results = data[result_categories]
    log.debug(shot_results.info())
    result_count = shot_results.notna().sum(axis=1)
    if (result_count < 1).any():
        log.warning('no shot result:\n%s', shot_results[result_count < 1])
    if (result_count > 1).any():
        log.debug('multiple shot results:\n%s', shot_results[result_count > 1])
    result = pd.Categorical([''] * len(shot_results.index), categories=result_categories)
    for label, content in shot_results.items():
        result[content.notna()] = label
    log.debug(pd.Series(result))
    log.debug(pd.Series(result).value_counts())
    out['sh_outc'] = pd.Series(result)

def parse_involved_players_for(data, out):
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
            log.warning('too many players, index : %d', index)
            log.debug(players_on)
    log.debug(players)
    for label, content in players.items():
        out[label] = content

def parse_involved_players_against(data, out):
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
            log.warning('too many players, index : %d', index)
            log.debug(players_on)
    log.debug(players)
    for label, content in players.items():
        out[label] = content

def parse_acting_players(data, out):
    """parse the acting players (shot, assist, block) from the columns with player numbers"""
    players_goalies = data.filter(regex=("^g?[0-9]+$"))
    actions = pd.DataFrame('', index=players_goalies.index, columns=['shot', 'assist', 'block'])
    for col in players_goalies:
        player = players_goalies[col].astype(str)
        nbr = col.replace('g', '')
        actions['shot'][player.str.match('S')] = nbr
        actions['assist'][player.str.match('A')] = nbr
        actions['block'][player.str.match('B')] = nbr
    log.debug(actions)
    log.debug(actions.info())
    for label, content in actions.items():
        out[label] = content

def parse_team(data, out):
    """parse the team (home/away) from two columns"""
    home_name = 'x'
    away_name = 'y'
    home_away = data[[home_name, away_name]]
    log.debug(home_away.info())
    log.debug(home_away.isnull().sum().sum() == len(home_away.index))
    team = pd.Series([''] * len(home_away.index))
    team[home_away[home_name].isnull()] = 'away'
    team[home_away[away_name].isnull()] = 'home'
    log.debug(team)
    out['team'] = team

def parse_period(data, out):
    """parse the period int-string into int (OT => 4)"""
    period = data['period']
    period.replace('OT', '4', inplace=True)
    log.debug(period.astype(int))
    out['per'] = period.astype(int)

def parse_time(data, out):
    """parse video time float-string into minutes and seconds"""
    time_as_str = data['time_vid'].astype(str)
    vd_m_s = time_as_str.str.split('.', expand=True)
    vd_m_s.set_axis(['vd_m', 'vd_s'], axis=1, inplace=True)
    log.debug(vd_m_s)
    for label, content in vd_m_s.items():
        out[label] = content

    time_as_str = data['time_game_m'].astype(str)
    gm_m = time_as_str.str.split('.', expand=True).iloc[:, 0]
    log.debug(gm_m)
    out['gm_m'] = gm_m

def main():
    """Launcher."""
#    log.basicConfig(level=log.DEBUG)

    log.debug('Number of arguments: %d arguments.', len(sys.argv))
    log.debug('Argument List: %s', str(sys.argv))

    datadir = 'data/'
    filename = 'x'
    datafile = datadir + filename + '.csv'
    log.debug(datafile)

    data = pd.read_csv(datafile, quotechar="'")
    log.debug(data)

    parsed = pd.DataFrame([], index=data.index)

    parse_time(data, parsed)
    parse_period(data, parsed)
    parse_team(data, parsed)
    parse_acting_players(data, parsed)
    parse_involved_players_for(data, parsed)
    parse_involved_players_against(data, parsed)
    parse_shot_result(data, parsed)
    parse_shot_type(data, parsed)
    parse_pre_shot_situation(data, parsed)

    log.debug(parsed)
    log.debug(parsed.info())
    parsed.to_pickle(datadir + filename + '.pkl.xz')

if __name__ == "__main__":
    main()
