import pandas as pd

#read in lineup data
lineup_data = pd.read_csv('~/capstone_project/data/lineup_data.csv')

#read in a set of player clusters
player_clusters = pd.read_csv('~/capstone_project/data/cluster_test.csv')

#convert the lineup ids to iterable
lineup_ids = []
for i in xrange(lineup_data.shape[0]):
    lineup = lineup_data['lineup_ids'].iloc[i].replace(' ','').split('-')
    lineup = [int(x) for x in lineup]
    lineup.sort()
    lineup_ids.append(lineup)
lineup_data['lineup_ids'] = lineup_ids
