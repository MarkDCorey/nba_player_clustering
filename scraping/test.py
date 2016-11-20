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
def unique_shots(id_lst):
    # id_lst = ['201935', '201142', '202326', '2544', '203081']
    lst = []
    for i in id_lst:
        chart = shotchart.ShotChart(i, season = '2015-16').shot_chart()
        chart['SHOT_GRP'] = chart['SHOT_TYPE'] + '_' + chart['ACTION_TYPE']
        lst.append(chart['SHOT_GRP'].unique())
#
    lst2 = [shot_type for item in lst for shot_type in item]
    unique_shots = set(lst2)
    return unique_shots



def get_player_ids(year = '2016-17', only_curr = 0):
    players = player.PlayerList(season = year, only_current = only_curr ).info()

    year_start = int(year[0:4])
    year_end = int('20'+year[-2:])

    players.FROM_YEAR = pd.to_numeric(players.FROM_YEAR)
    players.TO_YEAR = pd.to_numeric(players.TO_YEAR)

    player_ids = []
    for i in range(players.shape[0]):
        #if player's start yr is <= than the last yr of season AND his end yr >= first year of season
        if (players.FROM_YEAR.iloc[i] <= year_end) and (players.TO_YEAR.iloc[i] >= year_start):
            player_ids.append(players.PERSON_ID.iloc[i])
    player_ids.sort()
    return player_ids





def generate_player_shot_loc_df(player_id_list,year):
    lst_of_dicts = []

    for id in player_id_list:
        print id
        #get the shotchart for player
        shot_loc= player.PlayerShootingSplits(id, season = year).shot_areas()
        if not shot_loc.empty:
            attempt_RA = shot_loc.FGA[shot_loc.GROUP_VALUE == 'Restricted Area'].sum()
            made_RA = shot_loc.FGM[shot_loc.GROUP_VALUE == 'Restricted Area'].sum()

            attempt_paint = shot_loc.FGA[shot_loc.GROUP_VALUE == 'In The Paint (Non-RA)'].sum()
            made_paint = shot_loc.FGM[shot_loc.GROUP_VALUE == 'In The Paint (Non-RA)'].sum()

            attempt_mid = shot_loc.FGA[shot_loc.GROUP_VALUE == 'Mid-Range'].sum()
            made_mid = shot_loc.FGM[shot_loc.GROUP_VALUE == 'Mid-Range'].sum()

            attempt_corner_3 = (shot_loc.FGA[shot_loc.GROUP_VALUE == 'Left Corner 3'].sum()) + \
                (shot_loc.FGA[shot_loc.GROUP_VALUE == 'Right Corner 3'].sum())
            made_corner_3 = (shot_loc.FGM[shot_loc.GROUP_VALUE == 'Left Corner 3'].sum()) + \
                (shot_loc.FGM[shot_loc.GROUP_VALUE == 'Right Corner 3'].sum())

            attempt_non_corner_3 = (shot_loc.FGA[shot_loc.GROUP_VALUE == 'Above the Break 3'].sum()) + \
                (shot_loc.FGA[shot_loc.GROUP_VALUE == 'Backcourt'].sum())
            made_non_corner_3 = (shot_loc.FGM[shot_loc.GROUP_VALUE == 'Above the Break 3'].sum()) + \
                (shot_loc.FGM[shot_loc.GROUP_VALUE == 'Backcourt'].sum())

            lst_of_dicts.append({'player_id':str(id),'attempt_RA':attempt_RA,'made_RA':made_RA,
                                                     'attempt_paint':attempt_paint,'made_paint':made_paint,
                                                     'attempt_corner_3':attempt_corner_3,'made_corner_3':made_corner_3,
                                                     'attempt_non_corner_3':attempt_non_corner_3,'made_non_corner_3':made_non_corner_3,
                                                     'attempt_mid':attempt_mid,'made_mid':made_mid})

        else:
            lst_of_dicts.append({'player_id':str(id),'attempt_RA':0,'made_RA':0,
                                                     'attempt_paint':0,'made_paint':0,
                                                     'attempt_corner_3':0,'made_corner_3':0,
                                                     'attempt_non_corner_3':0,'made_non_corner_3':0,
                                                     'attempt_mid':0,'made_mid':0})
    player_shot_loc_df = pd.DataFrame(lst_of_dicts)
    player_shot_loc_df.set_index('player_id',inplace = True, drop=True)
    return player_shot_loc_df



def generate_ast_shot_df(player_id_list,year):
    lst_of_dicts = []

    for id in player_id_list:
        print id
        #get the shotchart for player
        ast_shots = player.PlayerShootingSplits(id, season = year).assisted_shots()
        if not ast_shots.empty:
            ast_shots_made = ast_shots.FGM[ast_shots.GROUP_VALUE == 'Assisted'].sum()

            lst_of_dicts.append({'player_id':str(id),'ast_shot_made':ast_shots_made})

        else:
            lst_of_dicts.append({'player_id':str(id),'ast_shot_made':0})

    ast_shot_df = pd.DataFrame(lst_of_dicts)
    ast_shot_df.set_index('player_id',inplace = True, drop=True)
    return ast_shot_df

# poss = FGA + 0.5 x FTA - ORB + TO

# player_ids = get_player_ids(year = '2015-16')
# test = generate_ast_shot_df(player_ids[:5],'2015-16')


lineups_2015_16 = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')

def generate_posessions_df(lineups):
    lineup_ids = []
    for i in xrange(lineups.shape[0]):
        lineup = lineups['lineup_ids'].iloc[i].replace(' ','').split('-')
        lineup = [int(x) for x in lineup]
        lineup.sort()
        lineup_ids.append(lineup)
    lineups['lineup_ids'] = lineup_ids
    lineups.drop('Unnamed: 0', inplace = True, axis = 1)

    lst_of_dicts = []
    for i in xrange(lineups.shape[0]):
        for id in lineups['lineup_ids'].iloc[i]:
            temp = {'id':id,
                    'FGA_l':float(lineups['FGA_l'].iloc[i]),
                    'FTA_l':float(lineups['FTA_l'].iloc[i]),
                    'OREB_l':float(lineups['OREB_l'].iloc[i]),
                    'TOV_l':float(lineups['TOV_l'].iloc[i])}
            lst_of_dicts.append(temp)

    pos_df = pd.DataFrame(lst_of_dicts)
    pos_df = pos_df.groupby(pos_df.id).sum()
    pos_df['pos'] = pos_df.FGA_l + (0.44 * pos_df.FTA_l) - pos_df.OREB_l + pos_df.TOV_l
    pos_df.drop(['FGA_l','FTA_l','OREB_l','TOV_l'], inplace = True, axis = 1)


    return pos_df

player_data = pd.read_csv('~/capstone_project/data/aggregated_player_data_15_16.csv')
player_data.set_index('player_id', inplace = True, drop = True)

pos_df = generate_posessions_df(lineups_2015_16)

merged_df = pd.concat([pos_df, player_data], axis=1)
