from nba_py import player
import pandas as pd

def create_csv(df, path):
    df.to_csv(path)
    return None



players_2015_16 = player.PlayerList(season = '2015-16', only_current=0).info()
create_csv(players_2015_16,'../data/players_2015_16.csv')
# players_2016_17 = player.PlayerList(season = '2016-17', only_current=0).info()
# players_2015_16 = player.PlayerList(season = '2015-16', only_current=0).info()
# players_2014_15 = player.PlayerList(season = '2014-15', only_current=0).info()
# players_2013_14 = player.PlayerList(season = '2013-14', only_current=0).info()
# players_2012_13 = player.PlayerList(season = '2012-13', only_current=0).info()
# players_2011_12 = player.PlayerList(season = '2011-12', only_current=0).info()
# players_2010_11 = player.PlayerList(season = '2010-11', only_current=0).info()
# players_2009_10 = player.PlayerList(season = '2009-10', only_current=0).info()
# players_2008_09 = player.PlayerList(season = '2008-09', only_current=0).info()
# players_2007_08 = player.PlayerList(season = '2007-08', only_current=0).info()
