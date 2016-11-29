from sklearn import decomposition
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler,normalize,scale
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

#read in the feature data and the initial cluster assignments
featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
big_clusters = pd.read_csv('~/capstone_project/data/big_clusters.csv')

big_cluster_1 = big_clusters['player_id'][big_clusters.cluster == 1].tolist()
big_cluster_2 = big_clusters['player_id'][big_clusters.cluster == 2].tolist()
big_cluster_3 = big_clusters['player_id'][big_clusters.cluster == 3].tolist()

#
player_mat_1 = featurized_data[featurized_data['player_id'].isin(big_cluster_1)]
player_info_1 = player_mat_1[['player_id','display_name']]
player_mat_1.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat_1.fillna(0, inplace = True)
player_mat_1 = normalize(player_mat_1)
pca_1 = decomposition.PCA(n_components=12)
pca_1_fit = pca_1.fit_transform(player_mat_1)
player_mat_1 = normalize(pca_1_fit)

kmeans_1 = KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
kmeans_1.fit_transform(player_mat_1)
cluster_labels_1 = kmeans_1.labels_
player_info_1['cluster'] = cluster_labels_1



player_mat_2 = featurized_data[featurized_data['player_id'].isin(big_cluster_2)]
player_info_2 = player_mat_2[['player_id','display_name']]
player_mat_2.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat_2.fillna(0, inplace = True)
player_mat_2 = normalize(player_mat_2)
pca_2 = decomposition.PCA(n_components=12)
pca_2_fit = pca_2.fit_transform(player_mat_2)
player_mat_2 = normalize(pca_2_fit)

kmeans_2 = KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
kmeans_2.fit_transform(player_mat_2)
cluster_labels_2 = kmeans_2.labels_
player_info_2['cluster'] = cluster_labels_2
player_info_2['cluster'].replace([0,1,2], [3,4,5], inplace=True)


player_mat_3 = featurized_data[featurized_data['player_id'].isin(big_cluster_3)]
player_info_3 = player_mat_3[['player_id','display_name']]
player_mat_3.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat_3.fillna(0, inplace = True)
player_mat_3 = normalize(player_mat_3)
pca_3 = decomposition.PCA(n_components=12)
pca_3_fit = pca_3.fit_transform(player_mat_3)
player_mat_3 = normalize(pca_3_fit)

kmeans_3 = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
kmeans_3.fit_transform(player_mat_3)
cluster_labels_3 = kmeans_3.labels_
player_info_3['cluster'] = cluster_labels_3
player_info_3['cluster'].replace([0,1,2,3], [6,7,8,9], inplace=True)



# #group the cluster_dfs
final_clusters = pd.concat([player_info_1, player_info_2, player_info_3])
composite_clusters = final_clusters.to_csv('~/capstone_project/data/composite_kmeans.csv')

#for finding the optimal k for each group...
# k_vals = [2,3,4,5,6,7]
# inertia_list = []
# for i in k_vals:
#     kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
#     precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
#     kmeans.fit_transform(player_mat_3)
#     cluster_labels = kmeans.labels_
#
#     s_score = silhouette_score(player_mat_3, cluster_labels, metric='euclidean',sample_size=None)
#     inertia_list.append(kmeans.inertia_)
#     print('k_val: ',i)
#     print('s_score: ',s_score)
#     print('total_inertia: ',kmeans.inertia_)
#     print
#
# plt.plot(k_vals, inertia_list)
# plt.xlabel('k')
# plt.ylabel('sum of error')
# plt.show()







#
#
#
#
#
