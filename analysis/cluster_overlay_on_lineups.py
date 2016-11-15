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

#create list to hold lists of clusters (later append this to df as a Series)
#iterate over each line in lineup_data
    #index into the linup_ids attribute
    #create empty temp list to hold clusters for each row
    #iterate over the lineup_ids list
    #for each id in the list to pull the corresponding cluster from player_clusters
        #add the cluster to the temp list
    #add the list to the list of clusters
#add the whole list of clusters to the df
