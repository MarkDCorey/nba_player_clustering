import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cluster_overlay import *

'''
INPUT: the featurized matrix used by model and the player cluster labels
OUTPUT: descriptions of each cluster - ranked features that define the cluster
'''




def get_feature_stats(feat_mat):

    '''
    get stats for each feature
    '''
    feat_mat_clean = feat_mat.iloc[:,4:]
    #for each feature get the mean and the standard deviation, add to df
    lst_of_dicts = []
    for feature in list(feat_mat_clean.columns):
        feat_std = np.std(feat_mat_clean[feature])
        feat_mean = np.mean(feat_mat_clean[feature])
        lst_of_dicts.append({'feature':feature,'feat_std':feat_std,
                         'feat_mean':feat_mean})

    feature_stats = pd.DataFrame(lst_of_dicts)
    return feature_stats


def cluster_feat_analyis(feat_stats, feat_clust_mat):

    lst_of_dicts = []

    clusters = feat_clust_mat.cluster.unique()
    #
    for cluster in clusters:
        cf_mat = feat_clust_mat[feat_clust_mat['cluster'] == cluster]

        for feat in feat_stats['feature'].values:
            cf_mean = np.mean(cf_mat[feat])
            feats_std = float(feat_stats['feat_std'][feat_stats['feature']== feat])
            feats_mean = float(feat_stats['feat_mean'][feat_stats['feature']== feat])
            std_from_avg = (cf_mean - feats_mean)/feats_std

            temp_d = {'cluster':cluster, 'feature':feat, 'cluster_mean':cf_mean,
                        'feature_mean':feats_mean, 'feature_std':feats_std, 'std_from_avg':std_from_avg}
            lst_of_dicts.append(temp_d)

    cluster_feat_df = pd.DataFrame(lst_of_dicts)
    return cluster_feat_df


def cluster_rank_features(cf_analysis_df, cluster):
    cluster_summary = cf_analysis_df[cf_analysis_df['cluster'] == cluster]
    sorted_cs = cluster_summary[['feature','std_from_avg']].sort(columns = 'std_from_avg',ascending=False)
    return sorted_cs



# player_clusters['cluster'][player_clusters['player_id'] == player_id]
# for cluster in





if __name__ == '__main__':
    FILE_FEATURES = 'data/featurized_data.csv'
    FILE_LINEUPS = '~/capstone_project/data/lineup_data.csv'
    FILE_CLUSTERS = '~/capstone_project/data/cluster_test.csv'
    #read in feature mat, the player clusters, and the linups
    featurized_mat = pd.read_csv(FILE_FEATURES)
    lineups = pd.read_csv(FILE_LINEUPS)
    player_clusters = pd.read_csv(FILE_CLUSTERS)


    #reduce the size of feat mat to match that of clusters
    ####
    minutes_min = 10
    ####

    featurized_mat = featurized_mat[featurized_mat.min_tot > minutes_min]

    #generate feature stats
    feature_stats = get_feature_stats(featurized_mat)

    #concat feats_players and clusters
    featurized_mat.set_index('player_id', inplace=True, drop = True)
    player_clusters.set_index('player_id', inplace = True, drop = True)
    feats_clusters = pd.concat([featurized_mat, player_clusters], axis=1)


    cluster_feat_df = cluster_feat_analyis(feature_stats, feats_clusters)

    for i in range(10):
        test = cluster_rank_features(cluster_feat_df, i)
        print'Cluster: ',i
        print'Top 10: ',test[['feature','std_from_avg']][:10]
        print ''

    #append clusters to

    # #
    # feats_and_clusters = add_clusters_to_lineups(lineups, player_clusters)
    # aggregate_clusters(feats_and_clusters)
