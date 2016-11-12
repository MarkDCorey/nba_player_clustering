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

# for year in seasons:
shot_type= shotchart.ShotChart('201939', season = '2015-16').shot_chart()

shots = shot_type[['ACTION_TYPE','SHOT_TYPE','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']] \
    .groupby(['ACTION_TYPE','SHOT_TYPE']).sum().reset_index()

shots['SHOT_GRP'] = shots['SHOT_TYPE'] + '_' + shots['ACTION_TYPE']

attempt_3 = shots.loc[shots['SHOT_TYPE']== '3PT Field Goal','SHOT_ATTEMPTED_FLAG'].sum()
attempt_2 = shots.loc[shots['SHOT_TYPE']== '2PT Field Goal','SHOT_ATTEMPTED_FLAG'].sum()
made_3 = shots.loc[shots['SHOT_TYPE']== '3PT Field Goal','SHOT_MADE_FLAG'].sum()
made_2 = shots.loc[shots['SHOT_TYPE']== '2PT Field Goal','SHOT_MADE_FLAG'].sum()

"""
used this to find the unique shot types
"""
# id_lst = ['201935', '201142', '202326', '2544', '203081']
# lst = []
# for i in id_lst:
#     chart = shotchart.ShotChart(i, season = '2015-16').shot_chart()
#     chart['SHOT_GRP'] = chart['SHOT_TYPE'] + '_' + chart['ACTION_TYPE']
#     lst.append(chart['SHOT_GRP'].unique())
# #
# lst2 = [shot_type for item in lst for shot_type in item]
# unique_shots = set(lst2)

attempt_drive_2 = shots.loc[(shots['SHOT_GRP']== '2PT Field Goal_Driving Bank Hook Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Bank shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Finger Roll Layup Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Floating Bank Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Floating Jump Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Layup Shot')| \
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
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Reverse Dunk Shot')| \
                            (shots['SHOT_GRP']== '2PT Field Goal_Driving Reverse Layup Shot'), \
                        'SHOT_MADE_FLAG'].sum()




#
# #two_at_the_rim
# '2PT Field Goal_Dunk Shot'
# '2PT Field Goal_Layup Shot'
# '2PT Field Goal_Tip Dunk Shot'
# '2PT Field Goal_Putback Dunk Shot',
# '2PT Field Goal_Putback Layup Shot'
# '2PT Field Goal_Reverse Dunk Shot',
# '2PT Field Goal_Reverse Layup Shot'
# '2PT Field Goal_Tip Layup Shot'
# '2PT Field Goal_Alley Oop Dunk Shot',
# '2PT Field Goal_Alley Oop Layup shot'
# '2PT Field Goal_Tip Layup Shot'
# '2PT Field Goal_Finger Roll Layup Shot'
# '2PT Field Goal_Running Alley Oop Dunk Shot',
# '2PT Field Goal_Running Dunk Shot',
# '2PT Field Goal_Running Finger Roll Layup Shot'
# '2PT Field Goal_Running Layup Shot'
# '2PT Field Goal_Cutting Dunk Shot',
# '2PT Field Goal_Cutting Finger Roll Layup Shot',
# '2PT Field Goal_Cutting Layup Shot'
# '2PT Field Goal_Running Reverse Dunk Shot'
# '2PT Field Goal_Running Reverse Layup Shot'
#
# #two_off_dribble
# '2PT Field Goal_Pullup Bank shot',
# '2PT Field Goal_Pullup Jump shot'
# '2PT Field Goal_Running Jump Shot'
# '2PT Field Goal_Running Pull-Up Jump Shot'
# '2PT Field Goal_Floating Jump shot',
#
# #two_jumper
# '2PT Field Goal_Jump Shot'
# '2PT Field Goal_Fadeaway Bank shot',
# '2PT Field Goal_Fadeaway Jump Shot',
# '2PT Field Goal_Jump Bank Shot',
# '2PT Field Goal_Jump Shot'
# '2PT Field Goal_Step Back Bank Jump Shot',
# '2PT Field Goal_Step Back Jump shot'
#
# #three_off_dribble
# '3PT Field Goal_Running Pull-Up Jump Shot'
# '3PT Field Goal_Pullup Jump shot'
# '3PT Field Goal_Running Jump Shot'
# '3PT Field Goal_Pullup Bank shot',
# '3PT Field Goal_Floating Jump shot'
#
# #two_post
# '2PT Field Goal_Turnaround Bank shot',
# '2PT Field Goal_Turnaround Fadeaway Bank Jump Shot',
# '2PT Field Goal_Turnaround Fadeaway shot',
# '2PT Field Goal_Turnaround Hook Shot',
# '2PT Field Goal_Turnaround Jump Shot'
# '2PT Field Goal_Hook Shot'
#
# #three_not_off_dribble
# '3PT Field Goal_Step Back Jump shot'
# '3PT Field Goal_Turnaround Jump Shot'
# '3PT Field Goal_Jump Shot'
# '3PT Field Goal_Jump Bank Shot'
# '3PT Field Goal_Fadeaway Jump Shot'
# '3PT Field Goal_Fadeaway Bank shot'
