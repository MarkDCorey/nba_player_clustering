import pandas as pd


def add_clusters_to_lineups(lineups_df, clusters_df):
    #convert the lineup ids to sorted list of ints
    lineup_ids = []
    for i in xrange(lineups_df.shape[0]):
        lineup = lineups_df['lineup_ids'].iloc[i].replace(' ','').split('-')
        lineup = [int(x) for x in lineup]
        lineup.sort()
        lineup_ids.append(lineup)
    lineups_df['lineup_ids'] = lineup_ids


    #create list of players that have cluster assignments
    players_with_cluster  = clusters_df.player_id.tolist()

    #create list to hold lists of clusters (later append this to df as a Series)
    cluster_lst = []
    #iterate over each line in lineup_data
    for i in xrange(lineups_df.shape[0]):
        #index into the linup_ids attribute
        lineup = lineups_df['lineup_ids'].iloc[i]

        #create empty temp list to hold clusters for each row
        clusters_temp = []

        #iterate over the lineup_ids list
        for player_id in lineup:
            print player_id
            if player_id in players_with_cluster:
                #for each id in the list to pull the corresponding cluster from player_clusters
                player_cluster = player_clusters['cluster'][player_clusters['player_id'] == player_id]
                clusters_temp.append(int(player_cluster.iloc[0]))
            else:
                clusters_temp.append('X')
        #add the cluster to the temp list
        clusters_temp.sort()
        clusters_temp = [str(x) for x in clusters_temp]
        #add the list to the list of clusters
        cluster_lst.append(clusters_temp)
    #add the whole list of clusters to the df
    lineups_df['clusters'] = cluster_lst
    return lineups_df

#group by cluster, create plus_minus col
def aggregate_clusters(lineup_cluster_df):
    clusters_str = lineup_cluster_df['clusters'].apply(lambda x: ', '.join(x))
    lineup_cluster_df['clusters_str'] = clusters_str
    lineup_cluster_df = lineup_cluster_df[['lineup_ids','lineup_names','clusters_str','points_scored','points_allowed']]
    lineup_cluster_df = lineup_cluster_df[lineup_cluster_df.clusters_str.str.contains("X") == False]
    grouped_clusters = lineup_cluster_df['clusters_str','points_scored','points_allowed'].groupby('clusters_str').sum()


    return grouped_clusters






#
#
#     grouped_df = lineup_cluster_df.groupby('clusters').sum()
#
#     # grouped_df['plus_minus'] = grouped_df['points_scored'] - grouped_df['points_allowed']
#     # grouped_df.sort(columns='plus_minus', ascending = False, inplace = True)
#
#     return grouped_df



if __name__ == '__main__':
    #read in lineup data and set of player clusters
    lineup_data = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')
    player_clusters = pd.read_csv('~/capstone_project/data/h_clusters_2015_16.csv')
    lineup_cluster_df = add_clusters_to_lineups(lineup_data,player_clusters)
    grouped_df = aggregate_clusters(lineup_cluster_df)
