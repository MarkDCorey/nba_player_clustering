from nba_py import _api_scrape, _get_json, player, league, game, shotchart, team, draftcombine, constants
import pandas as pd
import numpy as np
from datetime import datetime
import time

'''
1) generate a list of active players
2) scrape summary and performance information and merge into single df
3) store the data in a csv so it can be accessed directly by the model

# shot_type volume (eg attempts of shot_type per min) and efficiency.
# may need to impute 0 of N/A (if acceptable) for efficiency metric if volume is below a certain threshold

'''

#get a list of the player ids for a given season
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


def generate_player_summary_df(player_id_list):

    lst_of_dicts = []

    for id in player_id_list:
        print id
        player_summary = player.PlayerSummary(player_id = id).info()
        first_name = player_summary.FIRST_NAME.iloc[0]
        last_name = player_summary.LAST_NAME.iloc[0]
        display_name = player_summary.DISPLAY_FIRST_LAST.iloc[0]
        bday = player_summary.BIRTHDATE.iloc[0]
        bday = datetime.strptime(bday, '%Y-%m-%dT%H:%M:%S')
        age = (datetime.now() - bday).days
        ht = str(player_summary.HEIGHT.iloc[0])
        if ht:
            height_ft = int(ht.rsplit('-', 1)[0]) * 12
            if ht.rsplit('-',1)[1]:
                height_in = int(ht.rsplit('-',1)[1])
            else:
                height_in = 0
            height = height_ft + height_in
        else:
            height = 0
        wt = str(player_summary.WEIGHT.iloc[0])
        if wt:
            weight = int(wt)
        else:
            weight = 0
        seasons = player_summary.SEASON_EXP.iloc[0]
        position = player_summary.POSITION.iloc[0]
        roster_status = player_summary.ROSTERSTATUS.iloc[0]
        team_id = player_summary.TEAM_ID.iloc[0]
        team_name = player_summary.TEAM_NAME.iloc[0]
        d_league_flag = player_summary.DLEAGUE_FLAG.iloc[0]

        temp_dict = {'player_id': str(id), 'first_name':first_name,
                    'last_name':last_name,'display_name':display_name,
                    'age':int(age),'height':height,'weight':weight,'season_exp':int(seasons),
                    'position':position,'roster_status':roster_status,'team_id':str(team_id),
                    'team_name':team_name,'dleague_flag':d_league_flag}

        lst_of_dicts.append(temp_dict)
        # time.sleep(1)

    player_summary_df = pd.DataFrame(lst_of_dicts)
    player_summary_df.set_index('player_id',inplace = True, drop = True)

    return player_summary_df


def generate_player_shot_df(player_id_list,year):
    lst_of_dicts = []

    for id in player_id_list:
        print id
        #get the shotchart for player
        shot_type= shotchart.ShotChart(id, season = year).shot_chart()
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


def generate_catch_shoot_df(player_id_lst, year):
    lst_of_dicts = []
    for id in player_id_lst:
        print id
        shooting = player.PlayerShotTracking(id, season=year).general_shooting()
        if not shooting.empty and 'Catch and Shoot' in shooting.SHOT_TYPE.values:
            shooting.fillna(0,inplace=True)
            catch_shoot_freq = float(shooting.FGA_FREQUENCY[shooting.SHOT_TYPE == 'Catch and Shoot'])
            lst_of_dicts.append({'player_id':str(id), 'catch_shoot_freq':catch_shoot_freq})
            # time.sleep(1)
        else:
            lst_of_dicts.append({'player_id':str(id), 'catch_shoot_freq':0})

    catch_shoot_df = pd.DataFrame(lst_of_dicts)
    catch_shoot_df.set_index('player_id',inplace = True, drop = True)
    return catch_shoot_df


def generate_overalls_df(player_id_lst, year):
    lst_of_dicts = []
    for id in player_id_lst:
        print id
        stats = player.PlayerYearOverYearSplits(id).by_year()
        stats = stats[stats.GROUP_VALUE == year]
        if not stats.empty:
            gp = float(stats.GP)
            min_game = float(stats.MIN)
            ftm = float(stats.FTM)
            fta = float(stats.FTA)
            oreb = float(stats.OREB)
            dreb = float(stats.DREB)
            reb = float(stats.REB)
            ast = float(stats.AST)
            tov = float(stats.TOV)
            stl = float(stats.STL)
            blk = float(stats.BLK)
            blk_a = float(stats.BLKA)
            pfd = float(stats.PFD)
            pf = float(stats.PF)

            lst_of_dicts.append({'player_id':str(id),'gp':gp,'min_game':min_game,
                              'ftm':ftm,'fta':fta,'oreb':oreb,'dreb':dreb,
                              'reb':reb,'ast':ast,'tov':tov,'stl':stl,'blk':blk,
                              'blk_a':blk_a,'pfd':pfd,'pf':pf})
            # time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),'gp':0,'min_game':0,
                              'ftm':0,'fta':0,'oreb':0,'dreb':0,
                              'reb':0,'ast':0,'tov':0,'stl':0,'blk':0,
                              'blk_a':0,'pfd':0,'pf':0})
            # time.sleep(1)

    overalls_df = pd.DataFrame(lst_of_dicts)
    overalls_df.set_index('player_id',inplace = True, drop = True)
    return overalls_df


def generate_rebounding_df(player_id_lst,year):
    lst_of_dicts = []
    for id in player_id_lst:
        print id
        rebounding = player.PlayerReboundTracking(id, season=year).num_contested_rebounding()
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

def generate_speed_dist_df(player_id_lst,year):

    lst_of_dicts = []
    league_speed_dist = league.PlayerSpeedDistanceTracking(season = year).overall()

    for id in player_id_lst:
        print id
        player_speed_dist = league_speed_dist[league_speed_dist.PLAYER_ID == int(id)]
        if not player_speed_dist.empty:
            mi_game_tot = float(player_speed_dist.DIST_MILES)
            mi_game_off = float(player_speed_dist.DIST_MILES_OFF)
            mi_game_def = float(player_speed_dist.DIST_MILES_DEF)
            avg_speed_tot = float(player_speed_dist.AVG_SPEED)
            avg_speed_off = float(player_speed_dist.AVG_SPEED_OFF)
            avg_speed_def = float(player_speed_dist.AVG_SPEED_DEF)

            lst_of_dicts.append({'player_id':str(id),'mi_game_tot':mi_game_tot,
                             'mi_game_off':mi_game_off,'mi_game_def':mi_game_def,
                             'avg_speed_tot':avg_speed_tot,'avg_speed_off':avg_speed_off,
                             'avg_speed_def':avg_speed_def})
            # time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),'mi_game_tot':0,
                             'mi_game_off':0,'mi_game_def':0,
                             'avg_speed_tot':0,'avg_speed_off':0,
                             'avg_speed_def':0})
            # time.sleep(1)

    speed_dist_df = pd.DataFrame(lst_of_dicts)
    speed_dist_df.set_index('player_id',inplace = True, drop = True)
    return speed_dist_df


def generate_defense_df(player_id_lst,year):

    lst_of_dicts = []

    for id in player_id_lst:
        print id
        player_defense = player.PlayerDefenseTracking(id, season = year).overall()
        if not player_defense.empty:

            d_fgm_overall = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == 'Overall'])
            d_fga_overall = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == 'Overall'])

            d_fgm_paint = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == 'Less Than 6 Ft'])
            d_fga_paint = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == 'Less Than 6 Ft'])

            d_fgm_perim = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == 'Greater Than 15 Ft'])
            d_fga_perim = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == 'Greater Than 15 Ft'])

            d_fgm_mid = d_fgm_overall - d_fgm_perim - d_fgm_paint
            d_fga_mid = d_fga_overall - d_fga_perim - d_fga_paint

            d_fgm_threes = float(player_defense.D_FGM[player_defense.DEFENSE_CATEGORY == '3 Pointers'])
            d_fga_threes = float(player_defense.D_FGA[player_defense.DEFENSE_CATEGORY == '3 Pointers'])


            lst_of_dicts.append({'player_id':str(id),
                        'd_fgm_overall':d_fgm_overall,'d_fga_overall':d_fga_overall,
                        'd_fgm_paint':d_fgm_paint,'d_fga_paint':d_fga_paint,
                        'd_fgm_mid':d_fgm_mid,'d_fga_mid':d_fga_mid,
                        'd_fgm_perim':d_fgm_perim,'d_fga_perim':d_fga_perim,
                        'd_fgm_threes':d_fgm_threes,'d_fga_threes':d_fga_threes,
                        })
            # time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),
                        'd_fgm_overall':0,'d_fga_overall':0,
                        'd_fgm_paint':0,'d_fga_paint':0,
                        'd_fgm_mid':0,'d_fga_mid':0,
                        'd_fgm_perim':0,'d_fga_perim':0,
                        'd_fgm_threes':0,'d_fga_threes':0,

                        })


    defense_df = pd.DataFrame(lst_of_dicts)
    defense_df.set_index('player_id',inplace = True, drop = True)
    return defense_df


def generate_pass_df(player_id_lst, year):
    lst_of_dicts = []

    for id in player_id_lst:
        print id
        player_pass = player.PlayerPassTracking(id, season = year).passes_made()
        if not player_pass.empty:
            passes = (player_pass.PASS * player_pass.G)
            pass_total = passes.sum()
            lst_of_dicts.append({'player_id':str(id),'pass_total':float(pass_total)})
            # time.sleep(1)

        else:
            lst_of_dicts.append({'player_id':str(id),'pass_total':0})

    pass_df = pd.DataFrame(lst_of_dicts)
    pass_df.set_index('player_id',inplace = True, drop = True)
    return pass_df





if __name__ == '__main__':
    year = '2014-15'
    #create ordered list of player ids
    print 'Get player_ids'
    player_ids = get_player_ids(year = '2014-15')
    # player_ids = player_ids[:3]

    #clean and munge
    print 'Create summary_df'
    summary_df = generate_player_summary_df(player_ids)
    print 'Create shot_df'
    shot_df = generate_player_shot_df(player_ids,year)
    print 'Create catch_shoot_df'
    catch_shoot_df = generate_catch_shoot_df(player_ids, year)
    print 'Create overalls_df'
    overalls_df = generate_overalls_df(player_ids,year)
    print 'Create rebounding_df'
    rebounding_df = generate_rebounding_df(player_ids,year)
    print 'Create speed_dist_df'
    speed_dist_df = generate_speed_dist_df(player_ids, year)
    print 'Create defense_df'
    defense_df = generate_defense_df(player_ids, year)
    print 'Create pass_df'
    pass_df = generate_pass_df(player_ids, year)

    #create master df
    merged_df = pd.concat([summary_df, shot_df, catch_shoot_df, overalls_df, \
        rebounding_df, speed_dist_df, defense_df, pass_df], axis=1)

    #store df in csv
    merged_df.to_csv('~/capstone_project/data/aggregated_player_data_14_15.csv')
