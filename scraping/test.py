from nba_py import _api_scrape, _get_json, player, league, game, shotchart, team, draftcombine, constants
import pandas as pd
import numpy as np
from datetime import datetime
import time
from scrape import get_player_ids

#get list of ids to iterate over
player_ids = get_player_ids()


#want to get sufficient data but also maintain recency relevance of data
#test two or three most recent seasons
#remember that this must be linkable to lineup data. Eg, if i want to look
#back three seasons with the lineup data, i need my player id list to
#to include all players in the last three seasons, and i need the
#training set to do the same.
seasons = ['2016-17', '2015-16', '2014-15']

# """
# used this to find the unique shot types
# """
# # id_lst = ['201935', '201142', '202326', '2544', '203081']
# # lst = []
# # for i in id_lst:
# #     chart = shotchart.ShotChart(i, season = '2015-16').shot_chart()
# #     chart['SHOT_GRP'] = chart['SHOT_TYPE'] + '_' + chart['ACTION_TYPE']
# #     lst.append(chart['SHOT_GRP'].unique())
# # #
# # lst2 = [shot_type for item in lst for shot_type in item]
# # unique_shots = set(lst2)
#

# def genearate_catch_shoot_df(player_id_lst):
#     lst_of_dicts = []
#     for id in player_id_lst:
#         shooting = player.PlayerShotTracking(id, season='2015-16').general_shooting()
#         catch_shoot = shooting.loc[shooting['SHOT_TYPE'] == 'Catch and Shoot']
#     #     catch_shoot_freq = catch_shoot['FGA_FREQUENCY']
#     #     lst_of_dicts.append({'player_id':id, 'catch_shoot_freq':catch_shoot_freq})
#     # catch_shoot_df = pd.DataFrame(lst_of_dicts)
#     # return catch_shoot_df
#
# genearate_catch_shoot_df(player_ids[:10])
