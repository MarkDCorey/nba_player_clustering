from nba_py import team, constants

def get_team_ids():
    team_ids = []
    team_names = constants.TEAMS.keys()
    for team_id in team_names:
        team_ids.append(constants.TEAMS[team_id]['id'])
    return team_ids


if __name__ == '__main__':
    team_ids = get_team_ids()

# teams = team.TeamList.info()
