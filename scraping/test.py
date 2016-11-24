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
        shot_chart = shotchart.ShotChart(id, season = year).shot_chart()
        shots = shot_chart[['SHOT_ZONE_BASIC','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']].groupby('SHOT_ZONE_BASIC').sum()
        shots.reset_index(inplace = True)
        if not shots.empty:
            attempt_RA = shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'Restricted Area'].sum()
            made_RA = shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'Restricted Area'].sum()

            attempt_paint = shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'In The Paint (Non-RA)'].sum()
            made_paint = shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'In The Paint (Non-RA)'].sum()

            attempt_mid = shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'Mid-Range'].sum()
            made_mid = shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'Mid-Range'].sum()

            attempt_corner_3 = (shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'Left Corner 3'].sum()) + \
                (shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'Right Corner 3'].sum())
            made_corner_3 = (shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'Left Corner 3'].sum()) + \
                (shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'Right Corner 3'].sum())

            attempt_non_corner_3 = (shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'Above the Break 3'].sum()) + \
                (shots.SHOT_ATTEMPTED_FLAG[shots.SHOT_ZONE_BASIC == 'Backcourt'].sum())
            made_non_corner_3 = (shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'Above the Break 3'].sum()) + \
                (shots.SHOT_MADE_FLAG[shots.SHOT_ZONE_BASIC == 'Backcourt'].sum())

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


def generate_rebounding_df(player_id_lst,year):
    lst_of_dicts = []
    for id in player_id_lst:
        print id
        rebounding = player.PlayerReboundTracking(id, per_mode='PerPossession',season=year).num_contested_rebounding()
        if not rebounding.empty:
            c_oreb_game = float(rebounding.C_OREB.sum())
            c_dreb_game = float(rebounding.C_DREB.sum())

            lst_of_dicts.append({'player_id':str(id),'c_oreb_game':c_oreb_game,'c_dreb_game':c_dreb_game})
            # time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),'c_oreb_game':0,'c_dreb_game':0})

    rebounding_df = pd.DataFrame(lst_of_dicts)
    rebounding_df.set_index('player_id',inplace = True, drop = True)
    return rebounding_df

def generate_player_shot_df(player_id_list,year):
    lst_of_dicts = []

    for id in player_id_list:
        print id
        #get the shotchart for player
        shot_type= shotchart.ShotChart(id, per_mode='PerPossession',season = year).shot_chart()
        if not shot_type.empty:
            shots = shot_type[['ACTION_TYPE','SHOT_TYPE','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']] \
                .groupby(['ACTION_TYPE','SHOT_TYPE']).sum().reset_index()
            shots['SHOT_GRP'] = shots['SHOT_TYPE'] + '_' + shots['ACTION_TYPE']

        #define what we want to add to the df
            attempt_3 = shots.loc[shots['SHOT_TYPE']== '3PT Field Goal','SHOT_ATTEMPTED_FLAG'].sum()
            attempt_2 = shots.loc[shots['SHOT_TYPE']== '2PT Field Goal','SHOT_ATTEMPTED_FLAG'].sum()
            made_3 = shots.loc[shots['SHOT_TYPE']== '3PT Field Goal','SHOT_MADE_FLAG'].sum()
            made_2 = shots.loc[shots['SHOT_TYPE']== '2PT Field Goal','SHOT_MADE_FLAG'].sum()
            total_attempt = attempt_3 + attempt_2
            total_made = made_3 + made_2

            attempt_drive_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Driving Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Floating Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Floating Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Reverse Layup Shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_drive_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Driving Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Floating Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Floating Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Reverse Layup Shot'), \
                        'SHOT_MADE_FLAG'].sum()

            attempt_at_rim_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Tip Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Putback Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Putback Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Reverse Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Tip Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Alley Oop Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Alley Oop Layup shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Finger Roll Layup Shot'),\
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_at_rim_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Tip Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Putback Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Putback Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Reverse Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Tip Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Alley Oop Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Alley Oop Layup shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Finger Roll Layup Shot'),\
                        'SHOT_MADE_FLAG'].sum()

            attempt_cut_run_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Running Alley Oop Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Alley Oop Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Cutting Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Cutting Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Cutting Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Reverse Layup Shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_cut_run_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Running Alley Oop Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Alley Oop Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Cutting Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Cutting Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Cutting Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Reverse Layup Shot'), \
                        'SHOT_MADE_FLAG'].sum()

            attempt_off_dribble_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Pullup Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Pullup Jump shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Pull-Up Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Floating Jump shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_off_dribble_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Pullup Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Pullup Jump shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Running Pull-Up Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Floating Jump shot'), \
                        'SHOT_MADE_FLAG'].sum()

            attempt_jumper_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Fadeaway Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Fadeaway Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Jump Bank Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Jump shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Step Back Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Step Back Jump shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_jumper_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Fadeaway Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Fadeaway Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Jump Bank Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Jump shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Step Back Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Step Back Jump shot'), \
                        'SHOT_MADE_FLAG'].sum()

            attempt_post_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Turnaround Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Fadeaway Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Fadeaway shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Hook Bank Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Hook Shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_post_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Turnaround Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Fadeaway Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Fadeaway shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Hook Bank Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Turnaround Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Hook Shot'), \
                        'SHOT_MADE_FLAG'].sum()


            attempt_off_dribble_3 = shots.loc[(shots['SHOT_GRP']== '3PT Field Goal_Running Pull-Up Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Pullup Jump shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Running Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Pullup Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Floating Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Floating Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Floating Jump shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_off_dribble_3 = shots.loc[(shots['SHOT_GRP']== '3PT Field Goal_Running Pull-Up Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Pullup Jump shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Running Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Pullup Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Floating Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Driving Floating Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Floating Jump shot'), \
                        'SHOT_MADE_FLAG'].sum()

            attempt_jumper_3 = shots.loc[(shots['SHOT_GRP']== '3PT Field Goal_Step Back Jump shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Jump Bank Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Fadeaway Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Fadeaway Bank shot') |\
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Fadeaway Bank Jump Shot')|\
                            (shots['SHOT_GRP']== '3PT Field Goal_Step Back Bank Jump Shot')|\
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Fadeaway shot'), \
                        'SHOT_ATTEMPTED_FLAG'].sum()

            made_jumper_3 = shots.loc[(shots['SHOT_GRP']== '3PT Field Goal_Step Back Jump shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Jump Bank Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Fadeaway Jump Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Fadeaway Bank shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Fadeaway Bank Jump Shot')|\
                            (shots['SHOT_GRP']== '3PT Field Goal_Step Back Bank Jump Shot')|\
                            (shots['SHOT_GRP']== '3PT Field Goal_Turnaround Fadeaway shot'), \
                        'SHOT_MADE_FLAG'].sum()



            temp_dict = {'player_id': str(id),
                    'total_attempt':float(total_attempt),'total_made':float(total_made),
                    'attempt_2':float(attempt_2),'made_2':float(made_2),
                    'attempt_3':float(attempt_3), 'made_3':float(made_3),
                    'attempt_drive_2':float(attempt_drive_2), 'made_drive_2':float(made_drive_2),
                    'attempt_at_rim_2':float(attempt_at_rim_2), 'made_at_rim_2':float(made_at_rim_2),
                    'attempt_cut_run_2':float(attempt_cut_run_2),'made_cut_run_2':float(made_cut_run_2),
                    'attempt_off_dribble_2':float(attempt_off_dribble_2), 'made_off_dribble_2':float(made_off_dribble_2),
                    'attempt_jumper_2':float(attempt_jumper_2), 'made_jumper_2':float(made_jumper_2),
                    'attempt_off_dribble_3':float(attempt_off_dribble_3), 'made_off_dribble_3':float(made_off_dribble_3),
                    'attempt_jumper_3':float(attempt_jumper_3), 'made_jumper_3':float(made_jumper_3),
                    'attempt_post_2':float(attempt_post_2), 'made_post_2':float(made_post_2)
                    }
            lst_of_dicts.append(temp_dict)

        else:
            temp_dict_empty = {'player_id': str(id),
                    'total_attempt':float(0),'total_made':float(0),
                    'attempt_2':float(0),'made_2':float(0),
                    'attempt_3':float(0), 'made_3':float(0),
                    'attempt_drive_2':float(0), 'made_drive_2':float(0),
                    'attempt_at_rim_2':float(0), 'made_at_rim_2':float(0),
                    'attempt_cut_run_2':float(0),'made_cut_run_2':float(0),
                    'attempt_off_dribble_2':float(0), 'made_off_dribble_2':float(0),
                    'attempt_jumper_2':float(0), 'made_jumper_2':float(0),
                    'attempt_off_dribble_3':float(0), 'made_off_dribble_3':float(0),
                    'attempt_jumper_3':float(0), 'made_jumper_3':float(0),
                    'attempt_post_2':float(0), 'made_post_2':float(0)
                    }
            lst_of_dicts.append(temp_dict_empty)


            # time.sleep(1)

    player_shot_df = pd.DataFrame(lst_of_dicts)
    player_shot_df.set_index('player_id',inplace = True, drop=True)
    return player_shot_df

def generate_reb_pos_df(player_id_list,year):
    lst_of_dicts = []

    for id in player_id_list:
        print id
        stats = player.PlayerGeneralSplits(player_id = id, per_mode='PerPossession', season = year).overall()
        dreb_pos = stats['DREB'].sum()
        oreb_pos = stats['OREB'].sum()

        temp_dict = {'player_id': str(id),
                'dreb_pos':float(dreb_pos),'oreb_pos':float(oreb_pos)}

        lst_of_dicts.append(temp_dict)

    reb_pos_df = pd.DataFrame(lst_of_dicts)
    reb_pos_df.set_index('player_id',inplace = True, drop=True)
    return reb_pos_df


player_ids = get_player_ids(year = '2015-16')
pids = player_ids[:10]
test = generate_ast_shot_df(pids, year = '2015-16')
