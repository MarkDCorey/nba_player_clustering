import pandas as pd


######################################
#read in the yearly lineup data that should be merged
raw_lineup_data_2015_16 = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')
raw_lineup_data_2014_15 = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')
raw_lineup_data_dfs = [raw_lineup_data_2015_16, raw_lineup_data_2014_15]

#read in the player clusters
player_clusters = pd.read_csv('~/capstone_project/data/h_clusters_2015_16.csv')
#####################################
#
# def lineup_merge_test(raw_lineup_data_dfs):
#     merged_lineup_data_df = raw_lineup_data_dfs[0]
#     for i, df in enumerate(raw_lineup_data_dfs):
#         if i > 0:
#             merged_lineup_data_df = merged_lineup_data_df.append(df, ignore_index= True)
#     return merged_lineup_data_df
#
# test = lineup_merge_test(raw_lineup_data_dfs)


def add_clusters_to_lineups(raw_lineup_data_dfs, clusters_df):
    """
    INPUT:
    1) a list of dataframes of lineup data by season (ie one or more seasons)
    2) a dataframe of cluster assignments per player_id

    OUTPUT:
    1) a dataframe of every lineup transformed into cluster combinations

    """
    #convert the lineup ids to sorted list of ints
    lineups_df = raw_lineup_data_dfs[0]
    for i, df in enumerate(raw_lineup_data_dfs):
        if i > 0:
            lineups_df = lineups_df.append(df, ignore_index= True)

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

test = add_clusters_to_lineups(raw_lineup_data_dfs, player_clusters)

#group by cluster, create plus_minus col
def aggregate_clusters(lineup_cluster_df):

    '''
    INPUT:
    1) a dataframe of cluster combinations representing lineups and their stats
        (the output produced by 'add_clusters_to_lineups')
    OUTPUT:
    1) a dataframe of aggregated cluster combinations, sorted by net_plus_minus
    '''
    clusters_str = lineup_cluster_df['clusters'].apply(lambda x: ', '.join(x))
    lineup_cluster_df['clusters_str'] = clusters_str
    lineup_cluster_df = lineup_cluster_df[['lineup_ids','lineup_names','clusters_str','points_scored','points_allowed']]
    lineup_cluster_df = lineup_cluster_df[lineup_cluster_df.clusters_str.str.contains("X") == False]
    grouped_clusters = lineup_cluster_df[['clusters_str','points_scored','points_allowed']].groupby('clusters_str').sum()
    grouped_clusters['net'] = grouped_clusters['points_scored'] - grouped_clusters['points_allowed']
    grouped_clusters.sort('net', ascending = False, inplace = True)

    grouped_clusters.to_csv('~/capstone_project/data/clusters_lineups.csv')

    return grouped_clusters



# # if __name__ == '__main__':
#     #read in lineup data and set of player clusters
#     # lineup_data = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')
#     # player_clusters = pd.read_csv('~/capstone_project/data/h_clusters_2015_16.csv')
#     lineup_cluster_df = add_clusters_to_lineups(lineup_data,player_clusters)
# #     grouped_df = aggregate_clusters(lineup_cluster_df)
