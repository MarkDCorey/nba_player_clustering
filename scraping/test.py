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

def get_player_ids(year = '2016-17', only_curr = 0):
    players = player.PlayerList(season = year, only_current = only_curr ).info()

    year_start = int(year[0:4])
    year_end = int('20'+year[-2:])

    players.FROM_YEAR = pd.to_numeric(players.FROM_YEAR)
    players.TO_YEAR = pd.to_numeric(players.TO_YEAR)

    player_ids = []
    for i in range(players.shape[0]):
        if (players.FROM_YEAR.iloc[i] <= year_end) and (players.TO_YEAR.iloc[i] >= year_end):
            player_ids.append(players.PERSON_ID.iloc[i])
    player_ids.sort()
    return player_ids



def generate_defense_df(player_id_lst,year):

    lst_of_dicts = []

    for id in player_id_lst:
        player_defense = player.PlayerDefenseTracking(id, season = year).overall()
        if not player_defense.empty:

            d_fgm_overall = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == 'Overall'])
            d_fga_overall = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == 'Overall'])
            d_ppm_overall = float(player_defense.PCT_PLUSMINUS[player_defense.DEFENSE_CATEGORY == 'Overall'])

            d_fgm_paint = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == 'Less Than 6 Ft'])
            d_fga_paint = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == 'Less Than 6 Ft'])
            d_ppm_paint = float(player_defense.PCT_PLUSMINUS[player_defense.DEFENSE_CATEGORY == 'Less Than 6 Ft'])

            d_fgm_perim = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == 'Greater Than 15 Ft'])
            d_fga_perim = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == 'Greater Than 15 Ft'])
            d_ppm_perim = float(player_defense.PCT_PLUSMINUS[player_defense.DEFENSE_CATEGORY == 'Greater Than 15 Ft'])

            lst_of_dicts.append({'player_id':str(id),
                        'd_fgm_overall':d_fgm_overall,'d_fga_overall':d_fga_overall,'d_ppm_overall':d_ppm_overall,
                        'd_fgm_paint':d_fgm_paint,'d_fga_paint':d_fga_paint,'d_ppm_paint':d_ppm_paint,
                        'd_fgm_perim':d_fgm_perim,'d_fga_perim':d_fga_perim,'d_ppm_perim':d_ppm_perim
                        })
            time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),
                        'd_fgm_overall':0,'d_fga_overall':0,'d_ppm_overall':0,
                        'd_fgm_paint':0,'d_fga_paint':0,'d_ppm_paint':0,
                        'd_fgm_perim':0,'d_fga_perim':0,'d_ppm_perim':0
                        })


    defense_df = pd.DataFrame(lst_of_dicts)
    defense_df.set_index('player_id',inplace = True, drop = True)
    return defense_df

player_ids = get_player_ids('2015-16')
test = generate_defense_df(player_ids,'2015-16')

# ['201935','101249','201593']

#
# if __name__ == '__main__':
#     #create ordered list of player ids
#
