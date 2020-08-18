#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generating a boxscore view/chart/table from a single game."""

# Here comes your imports
import sys
import logging as log
import pandas as pd

# Here comes your (few) global variables

# Here comes your class definitions

# Here comes your function definitions
def get_player_and_goalie_count(players):
    """get count of players and goalies"""
    log.debug(players)
    reg_p = r'^(\d+|\?)$'
    reg_g = r'^(g\d+|g\?)$'
    lam_p = lambda col: col.str.contains(reg_p, regex=True, na=False)
    lam_g = lambda col: col.str.contains(reg_g, regex=True, na=False)
    out = pd.DataFrame([], index=players.index)
    out['players'] = players.apply(lam_p, axis=1).sum(axis=1)
    out['goalies'] = players.apply(lam_g, axis=1).sum(axis=1)
    return out

def get_strength(goals):
    """get the strenght (even, pp, pk) from the goals data"""
    team = goals['team']
    log.debug(team)

    col = ['hm_' + str(i) for i in range(1, 7)]
    pl_home = goals[col]
    log.debug(get_player_and_goalie_count(pl_home))
    col = ['aw_' + str(i) for i in range(1, 7)]
    pl_away = goals[col]
    log.debug(get_player_and_goalie_count(pl_away))

def main():
    """Launcher."""
#    log.basicConfig(level=log.DEBUG)

    log.debug('Number of arguments: %d arguments.', len(sys.argv))
    log.debug('Argument List: %s', str(sys.argv))

    datadir = 'data/'
    filename = 'x'
    datafile = datadir + filename + '.pkl.xz'
    log.debug(datafile)

    data = pd.read_pickle(datafile)
    log.debug(data.info())

    goals = data[data['sh_outc'] == 'G']
    print(goals)

    get_strength(goals)

if __name__ == "__main__":
    main()
