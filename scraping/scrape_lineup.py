from nba_py import team, constants
import pandas as pd

'''
pulls, merges and persists lineup performance data by season
'''

#list of team ids
def get_team_ids():
    team_ids = []
    team_names = constants.TEAMS.keys()
    for team_id in team_names:
        team_ids.append(constants.TEAMS[team_id]['id'])
    return team_ids

def get_lineups(team_id_lst,season = '2016-17'):
    lst_of_dicts = []
    for i in team_id_lst:
        team_lineups = team.TeamLineups(team_id = i, season = season).lineups()
        for j in range(team_lineups.shape[0]):
            lineup_ids = team_lineups.iloc[j]['GROUP_ID']
            lineup_names = team_lineups.iloc[j]['GROUP_NAME']
            points_scored = float(team_lineups.iloc[j]['PTS'])
            points_allowed = points_scored - float(team_lineups.iloc[j]['PLUS_MINUS'])
            GP = float(team_lineups.iloc[j]['GP'])
            MIN = float(team_lineups.iloc[j]['MIN'])
            FGA = float(team_lineups.iloc[j]['FGA'])
            FTA = float(team_lineups.iloc[j]['FTA'])
            OREB = float(team_lineups.iloc[j]['OREB'])
            TOV = float(team_lineups.iloc[j]['TOV'])

            lst_of_dicts.append({'lineup_ids':lineup_ids,'lineup_names':lineup_names,
                                 'points_scored':points_scored,
                                 'points_allowed':points_allowed,
                                 'FGA_l':(FGA * GP),
                                 'FTA_l':(FTA * GP),
                                 'OREB_l':(OREB * GP),
                                 'TOV_l':(TOV * GP),
                                 'MIN_TOT':(MIN*GP)})

    lineups_df = pd.DataFrame(lst_of_dicts)
    return lineups_df

# poss = FGA + 0.5 x FTA - ORB + TO



if __name__ == '__main__':
    year = '2012-13'
    team_ids = get_team_ids()
    lineups_df = get_lineups(team_ids, season=year)
    lineups_df.to_csv('~/capstone_project/data/lineup_data_2012_13.csv')
