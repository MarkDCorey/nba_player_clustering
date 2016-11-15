import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

#kmeans
# KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
#     precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
# kmeans.fit()
# kmeans.labels_




# #look for interpretability in the clusters.
# #ideally there is significant separation (eg standard dev from average of player set) on a subset of features
# #either use these features to define the cluster labels, or come up with own
#
# print "cluster centers:"
# print kmeans.cluster_centers_
#
# top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
# print "top features for each cluster:"
# for num, centroid in enumerate(top_centroids):
#     print "%d: %s" % (num, ", ".join(features[i] for i in centroid))



if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
    test = featurized_data[featurized_data.min_game >0]
    test_players = test[['player_id','display_name']]
    test.drop(['player_id','display_name'], inplace = True, axis = 1)
    test.fillna(0, inplace = True)
    KMeans_test = KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
    precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
    KMeans_test.fit(test)
