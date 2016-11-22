import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind as t
# from cluster_overlay import *
from pprint import pprint


'''
INPUT: the featurized matrix used by model and the player cluster labels
OUTPUT: descriptions of each cluster - ranked features that define the cluster
'''



def get_feature_stats(feat_mat, minimum_min =500):

    '''
    Gets mean and standard deviation for each feature

    INPUT: the feature matrix used to build the model, minimum number of minutes for each
            player included in analysis

    OUTPUT: a df of the STD and mean for each feature
    '''

    feat_mat = feat_mat[feat_mat['min_tot'] > minimum_min]
    feat_mat_clean = feat_mat.drop(['player_id','display_name','min_tot','gp'], axis = 1)
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



def get_stat_significance():
    ts, p = t(a,b, equal_var = False)



if __name__ == '__main__':
    #read in feature mat, the player clusters, and the linups
    featurized_mat = pd.read_csv('~/capstone_project/data/featurized_data.csv')
    player_clusters = pd.read_csv('~/capstone_project/data/h_clusters_2015_16.csv')

    #get feature stats
    feature_stats = get_feature_stats(featurized_mat, minimum_min =500)

    #concat feature matrix with clusters
    featurized_mat.set_index('player_id', inplace=True, drop = True)
    player_clusters.set_index('player_id', inplace = True, drop = True)
    features_clusters = player_clusters.merge(featurized_mat,how = 'left',left_index = True, right_index = True, sort = True)

    cluster_feat_df = cluster_feat_analyis(feature_stats, features_clusters)

    for i in range(16):
        test = cluster_rank_features(cluster_feat_df, i)
        print '    Cluster:',i
        pprint(test)
        print
        # pprint('Cluster: ',{}).format(i)
        # pprint('Features: ',test[['feature','std_from_avg']])
        # pprint('')
