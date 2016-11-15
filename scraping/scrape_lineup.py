from nba_py import team, constants
import pandas as pd

#list of team ids
def get_team_ids():
    team_ids = []
    team_names = constants.TEAMS.keys()
    for team_id in team_names:
        team_ids.append(constants.TEAMS[team_id]['id'])
    return team_ids

def get_lineups(team_id_lst,season = '2015-16'):
    lst_of_dicts = []
    for i in team_id_lst:
        team_lineups = team.TeamLineups(team_id = i).lineups()
        for j in range(team_lineups.shape[0]):
            lineup_ids = team_lineups.iloc[j]['GROUP_ID']
            lineup_names = team_lineups.iloc[j]['GROUP_NAME']
            points_scored = float(team_lineups.iloc[j]['PTS'])
            points_allowed = points_scored - float(team_lineups.iloc[j]['PLUS_MINUS'])

            lst_of_dicts.append({'lineup_ids':lineup_ids,'lineup_names':lineup_names,
                                 'points_scored':points_scored,
                                 'points_allowed':points_allowed})

    lineups_df = pd.DataFrame(lst_of_dicts)
    return lineups_df




if __name__ == '__main__':
    year = '2015-16'
    team_ids = get_team_ids()
    lineups_df = get_lineups(team_ids, season=year)
    lineups_df.to_csv('~/capstone_project/data/lineup_data.csv')
