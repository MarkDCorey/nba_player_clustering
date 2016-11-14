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


def generate_pass_df(player_id_lst, year):
    lst_of_dicts = []

    for id in player_id_lst:
        player_pass = player.PlayerPassTracking(id, season = year).passes_made()
        if not player_pass.empty:
            passes = (player_pass.PASS * player_pass.G)
            pass_total = passes.sum()
            lst_of_dicts.append({'player_id':str(id),'pass_total':float(pass_total)})
            time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),'pass_total':0})

    pass_df = pd.DataFrame(lst_of_dicts)
    pass_df.set_index('player_id',inplace = True, drop = True)
    return pass_df


# test = get_player_ids('2015-16',  only_curr = 0)

##### GET REACH DATA
### REGRESSION ANALYSIS - eg attributes like height and reach on rebounding


def generate_catch_shoot_df(player_id_lst, year):
    lst_of_dicts = []
    for id in player_id_lst:
        shooting = player.PlayerShotTracking(id, season=year).general_shooting()
        if not shooting.empty:
            catch_shoot_freq = float(shooting.FGA_FREQUENCY[shooting.SHOT_TYPE == 'Catch and Shoot'])
            lst_of_dicts.append({'player_id':str(id), 'catch_shoot_freq':catch_shoot_freq})
            time.sleep(1)
        else:
            lst_of_dicts.append({'player_id':str(id), 'catch_shoot_freq':0})

    catch_shoot_df = pd.DataFrame(lst_of_dicts)
    catch_shoot_df.set_index('player_id',inplace = True, drop = True)
    return catch_shoot_df


test = generate_catch_shoot_df(['201935','101249'],'2015-16')
#101249

#
# if __name__ == '__main__':
#     #create ordered list of player ids
#
