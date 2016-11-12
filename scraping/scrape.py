from nba_py import _api_scrape, _get_json, player, league, game, shotchart, team, draftcombine, constants
import pandas as pd
import numpy as np
from datetime import datetime
import time

'''
1) generate a list of active players
2) scrape summary and performance information and merge into single df
3) store the data in a csv so it can be accessed directly by the model
'''

#get a list of all the active player ids
players_2016_17 = player.PlayerList(season = '2016-17', only_current = 1).info()
player_ids = [players_2016_17.PERSON_ID.iloc[i] for i in range(players_2016_17.shape[0])]
player_ids.sort()

#FEATURES
#summary info...
def append_player_summary_info(df, player_id_list):
    for id in player_id_list:
        player_summary = player.PlayerSummary(player_id = id).info()
        first_name = player_summary.FIRST_NAME.iloc[0]
        last_name = player_summary.LAST_NAME.iloc[0]
        display_name = player_summary.DISPLAY_FIRST_LAST.iloc[0]
        bday = player_summary.BIRTHDATE.iloc[0]
        bday = datetime.strptime(bday, '%Y-%m-%dT%H:%M:%S')
        age = (datetime.now() - bday).days
        seasons = player_summary.SEASON_EXP.iloc[0]
        position = player_summary.POSITION.iloc[0]
        roster_status = player_summary.ROSTERSTATUS.iloc[0]
        team_id = player_summary.TEAM_ID.iloc[0]
        team_name = player_summary.TEAM_NAME.iloc[0]
        d_league_flag = player_summary.DLEAGUE_FLAG.iloc[0]
        temp_dict = {'player_id': str(int(id)), 'first_name':first_name,
                    'last_name':last_name,'display_name':display_name,
                    'age':int(age), 'season_exp':int(seasons),'position':position,
                    'roster_status':roster_status,'team_id':str(team_id),
                    'team_name':team_name,'dleague_flag':d_league_flag}
        df = df.append(temp_dict, ignore_index = True)
        time.sleep(1)

    return df





if __name__ == '__main__':
    #create empty master df
    player_summary_data = pd.DataFrame(columns = ['player_id', 'first_name',
                                              'last_name', 'display_name',
                                              'age', 'season_exp', 'position',
                                              'roster_status', 'team_id',
                                              'team_name', 'dleague_flag'])
    #scrape summary data and append to master df
    summary_df = append_player_summary_info(player_summary_data, player_ids[:5])
