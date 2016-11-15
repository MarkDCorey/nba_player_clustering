from nba_py import team, constants

#list of team ids
def get_team_ids():
    team_ids = []
    team_names = constants.TEAMS.keys()
    for team_id in team_names:
        team_ids.append(constants.TEAMS[team_id]['id'])
    return team_ids

def get_lineups(team_id_lst):
    team_lineups = []
    for team in team_id_lst:
        team_lineup = team.TeamLineups(team_id = team).lineups()
        




if __name__ == '__main__':
    team_ids = get_team_ids()

# teams = team.TeamList.info()
