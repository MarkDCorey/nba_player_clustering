from nba_py import _api_scrape, _get_json, player, league, game, shotchart, team, draftcombine, constants
import pandas as pd
import numpy as np
from datetime import datetime

'''
#master DataFrame for player features

player_data = pd.DataFrame(
    columns = ['player_id','player_name','player_age',... ])


#loop over a bunch of lists to build the df

for i in range(len(player_ids)):
    player_data.loc[i] = [player_ids[i],
                          player_names[i]
                          player_ages[i]
                          ]
'''


#get a list of all the active player ids

players_2016_17 = player.PlayerList(season = '2016-17', only_current = 1).info()
#454 ids...
player_ids = [players_2016_17.PERSON_ID.iloc[i] for i in range(players_2016_17.shape[0])]
player_ids.sort()

#FEATURES
# create list of ages
player_ages = []
# for id in player_ids:
player_summary = player.PlayerSummary(player_id = 2733).info()
bday = player_summary['BIRTHDATE'].iloc[0]
