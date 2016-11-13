from nba_py import _api_scrape, _get_json, player, league, game, shotchart, team, draftcombine, constants
import pandas as pd
import numpy as np
from datetime import datetime
import time
from scrape import get_player_ids



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


player_ids = get_player_ids()

# def generate_overalls_df(player_id_lst, year):
#     lst_of_dicts = []
#     for id in player_id_lst:
#         stats = player.PlayerYearOverYearSplits(id).by_year()
#         gp = float(stats.GP[stats.GROUP_VALUE == year])
#         min_game = float(stats.MIN[stats.GROUP_VALUE == year])
#         ftm = float(stats.FTM[stats.GROUP_VALUE == year])
#         fta = float(stats.FTA[stats.GROUP_VALUE == year])
#         oreb = float(stats.OREB[stats.GROUP_VALUE == year])
#         dreb = float(stats.DREB[stats.GROUP_VALUE == year])
#         reb = float(stats.REB[stats.GROUP_VALUE == year])
#         ast = float(stats.AST[stats.GROUP_VALUE == year])
#         tov = float(stats.TOV[stats.GROUP_VALUE == year])
#         stl = float(stats.STL[stats.GROUP_VALUE == year])
#         blk = float(stats.BLK[stats.GROUP_VALUE == year])
#         blk_a = float(stats.BLKA[stats.GROUP_VALUE == year])
#         pfd = float(stats.PFD[stats.GROUP_VALUE == year])
#         pf = float(stats.PF[stats.GROUP_VALUE == year])
#
#         lst_of_dicts.append({'player_id':id,'gp':gp,'min_game':min_game,
#                               'ftm':ftm,'fta':fta,'oreb':oreb,'dreb':dreb,
#                               'reb':reb,'ast':ast,'tov':tov,'stl':stl,'blk':blk,
#                               'blk_a':blk_a,'pfd':pfd,'pf':pf})
#         time.sleep(1)
#
#     overalls_df = pd.DataFrame(lst_of_dicts)
#     return overalls_df
#
# test = generate_overalls_df(player_ids[:5], '2015-16')



def generate_rebounding_df(player_id_lst,year):
    lst_of_dicts = []
    for id in player_id_lst:
        rebounding = player.PlayerReboundTracking(id, season=year).num_contested_rebounding()
        c_oreb_game = float(rebounding.C_OREB.sum())
        c_dreb_game = float(rebounding.C_DREB.sum())

        lst_of_dicts.append({'player_id':id,'c_oreb_game':c_oreb_game,'c_dreb_game':c_dreb_game})
        time.sleep(1)
    rebounding_df = pd.DataFrame(lst_of_dicts)
    return rebounding_df

test = generate_rebounding_df(['201939'], '2015-16')









#
# if __name__ == '__main__':
#     #create ordered list of player ids
#
