import pandas as pd


######################################
#read in the yearly lineup data that should be merged for analysis
raw_lineup_data_2016_17 = pd.read_csv('~/capstone_project/data/lineup_data_2016_17.csv')
raw_lineup_data_2015_16 = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')
raw_lineup_data_2014_15 = pd.read_csv('~/capstone_project/data/lineup_data_2014_15.csv')
raw_lineup_data_2013_14 = pd.read_csv('~/capstone_project/data/lineup_data_2013_14.csv')

raw_lineup_data_dfs = [raw_lineup_data_2016_17,raw_lineup_data_2015_16, raw_lineup_data_2014_15,raw_lineup_data_2013_14]

#read in the player clusters (model output)
player_clusters = pd.read_csv('~/capstone_project/data/h_clusters_2015_16.csv')
#####################################



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

def get_stat_significance(cluster_lineup_df, lineup_minute_min):
    #takes in file/df of all cluster combinations
    clusters_lineups = cluster_lineup_df

    #convert clusters to str so they can be grouped, drop unnecessary columns
    #drop any cluster combos containing players that aren't being included in analyis (ie low minutes played)
    #group by lineup ids (to aggregate lineup stats over multiple seasons)
    #create net rating column and net per min
    clusters_str = clusters_lineups['clusters'].apply(lambda x: ', '.join(x))
    clusters_lineups['clusters'] = clusters_str
    clusters_lineups = clusters_lineups[['lineup_ids','lineup_names','clusters','points_scored','points_allowed']]
    clusters_lineups = clusters_lineups[clusters_lineups.clusters.str.contains("X") == False]
    clusters_lineups = clusters_lineups.groupby('lineup_ids').sum()
    clusters_lineups['net'] = clusters_lineups['points_scored'] - clusters_lineups['points_allowed']
    clusters_lineups['net_per_min'] = clusters_lineups['net_rating']/clusters_lineups['MIN_TOT']
    clusters_lineups = clusters_lineups[clusters_lineups.MIN_TOT >= lineup_minute_min]

    #create set of all unique cluster combos
    unique_clusters = set(clusters_lineups['clusters'].tolist())

    #create an array over the df of the net_plus_minus/min for each lineup
    net_min_cluster_combo_all = clusters_lineups['net_per_min'].tolist()

    #iterate over the set, index into the df for that cluster combo (eg filter out everything else)
    # create an array representing the net_plus_minus/min for that cluster combo
    # run a welsh's t-test for each using the cluster combo array and the overall array
    #store scores

    lst_of_dicts = []
    for cluster in unique_clusters:
        net_min_cluster_combo = clusters_lineups['net_per_min'][clusters_lineups['clusters'] == cluster].tolist()
        t_score, p_val = t(net_min_cluster_combo_all,net_min_cluster_combo, equal_var = False)
        temp_dict = {'cluster_combo':cluster,'t_score':t_score, 'p_val':p_val}
        lst_of_dicts.append(temp_dict)

    cluster_combo_scores = pd.DataFrame(lst_of_dicts)

    return cluster_combo_scores


lineup_cluster_df = add_clusters_to_lineups(lineup_data,player_clusters)
test = get_stat_significance(lineup_cluster_df)





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





# # # if __name__ == '__main__':
#     #read in lineup data and set of player clusters
#     # lineup_data = pd.read_csv('~/capstone_project/data/lineup_data_2015_16.csv')
#     # player_clusters = pd.read_csv('~/capstone_project/data/h_clusters_2015_16.csv')
#     lineup_cluster_df = add_clusters_to_lineups(lineup_data,player_clusters)
#     cluster_combo_stats = get_stat_significance(lineup_cluster_df)
# #     grouped_df = aggregate_clusters(lineup_cluster_df)
