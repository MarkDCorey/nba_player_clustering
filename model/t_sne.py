import numpy as np
import pandas as pd

import matplotlib as mpl

# mpl.use('TkAgg')

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn import decomposition, datasets,ensemble, manifold, random_projection, metrics
from sklearn.preprocessing import StandardScaler,normalize,scale
from sklearn.cluster import KMeans


# featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
# player_mat = featurized_data[featurized_data.min_tot >200]
# player_info = player_mat[['player_id','display_name']]
# player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
# player_mat.fillna(0, inplace = True)
# player_mat = normalize(player_mat)
# #
#
# pca = decomposition.PCA(n_components=8) #, whiten=True
# player_mat = pca.fit_transform(player_mat)
# # player_mat = normalize(player_mat)
# #
# clustered = pd.read_csv('~/capstone_project/data/clustered_players.csv')
# clusters = np.asarray(clustered.cluster)



def visualize_t_sne(player_mat, clusters):
    # load up data
    data = player_mat
    x_data = data
    y_data = clusters



    RS = 20150101

    # perform t-SNE embedding
    vis_data = TSNE(random_state=RS).fit_transform(data)

    # plot the result
    vis_x = vis_data[:, 0]
    vis_y = vis_data[:, 1]

    plt.scatter(vis_x, vis_y) #c=y_data) #, cmap=plt.cm.get_cmap("jet", 3))
    # plt.colorbar(ticks=range(10))
    # plt.clim(-0.5, 9.5)
    plt.savefig("t_sne_10.png", dpi= 300)
    plt.show()


#read in the feature data and the initial cluster assignments
featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
big_clusters = pd.read_csv('~/capstone_project/data/big_clusters.csv')

big_cluster_1 = big_clusters['player_id'][big_clusters.cluster == 1].tolist()
big_cluster_2 = big_clusters['player_id'][big_clusters.cluster == 2].tolist()
big_cluster_3 = big_clusters['player_id'][big_clusters.cluster == 3].tolist()


player_mat_3 = featurized_data[featurized_data['player_id'].isin(big_cluster_3)]
player_info_3 = player_mat_3[['player_id','display_name']]
player_mat_3.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat_3.fillna(0, inplace = True)
# player_mat_1 = scale(player_mat_1)

pca = decomposition.PCA(n_components=4) #, whiten=True
pca_fit_3 = pca.fit_transform(player_mat_3)

var_ex = pca.explained_variance_ratio_
tot_var_ex = np.array([sum(var_ex[0:i+1]) for i,x in enumerate(var_ex)])

plt.figure(figsize=(12,4))
# plt.title("PCA", fontsize=14)

plt.subplot(1,2,1)
plt.plot(range(1,len(tot_var_ex)+1), tot_var_ex*100,'o-')
plt.axis([0, len(tot_var_ex)+1, 0, 100])
plt.xlabel('Components Included', fontsize = 14)
plt.ylabel('Cumulative % of variance explained', fontsize = 14)


plt.subplot(1,2,2)
plt.plot(range(1,len(var_ex)+1), var_ex*100,'o-')
plt.axis([0, len(var_ex)+1, 0, 100])
plt.xlabel('Component Number', fontsize = 14)
plt.ylabel('% of variance explained by component', fontsize = 14)
plt.savefig("PCA.png", dpi= 300)


plt.show()


t_sne_3 = TSNE(n_components = 3, perplexity = 7, learning_rate = 300)
player_mat_3_t = t_sne_3.fit_transform(pca_fit_3)
player_mat_3_t_scaled = scale(player_mat_3_t)

kmeans_3 = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
kmeans_3.fit_transform(player_mat_3_t)
cluster_labels_3 = kmeans_3.labels_
player_info_3['cluster'] = cluster_labels_3


data = player_mat_3_t
x_data = data
y_data = cluster_labels_3


# perform t-SNE embedding
vis_data = data

# plot the result
vis_x = vis_data[:, 0]
vis_y = vis_data[:, 1]

plt.scatter(vis_x, vis_y, c=y_data, cmap=plt.cm.get_cmap("jet", 4))
# plt.colorbar(ticks=range(10))
# plt.clim(-0.5, 9.5)
# plt.savefig("t_sne_10.png", dpi= 300)
plt.show()





# pca = decomposition.PCA(n_components=15) #, whiten=True
# pca_fit = pca.fit_transform(player_mat_2)
#
# var_ex = pca.explained_variance_ratio_
# tot_var_ex = np.array([sum(var_ex[0:i+1]) for i,x in enumerate(var_ex)])
#
# plt.figure(figsize=(12,4))
# # plt.title("PCA", fontsize=14)
#
# plt.subplot(1,2,1)
# plt.plot(range(1,len(tot_var_ex)+1), tot_var_ex*100,'o-')
# plt.axis([0, len(tot_var_ex)+1, 0, 100])
# plt.xlabel('Components Included', fontsize = 14)
# plt.ylabel('Cumulative % of variance explained', fontsize = 14)
#
#
# plt.subplot(1,2,2)
# plt.plot(range(1,len(var_ex)+1), var_ex*100,'o-')
# plt.axis([0, len(var_ex)+1, 0, 100])
# plt.xlabel('Component Number', fontsize = 14)
# plt.ylabel('% of variance explained by component', fontsize = 14)
# plt.savefig("PCA.png", dpi= 300)
#
#
# plt.show()



# player_mat_2 = featurized_data[featurized_data['player_id'].isin(big_cluster_2)]
# player_info_2 = player_mat_2[['player_id','display_name']]
# player_mat_2.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
# player_mat_2.fillna(0, inplace = True)
# player_mat_2 = scale(player_mat_2)
#
# pca = decomposition.PCA(n_components=9) #, whiten=True
# pca_fit = pca.fit_transform(player_mat_2)
#
#
# t_sne_2 = TSNE(n_components = 9)
# player_mat_2_t = t_sne_2.fit_transform(pca_fit)
# player_mat_2_t = scale(player_mat_2_t)
#
# kmeans_2 = KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
# precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
# kmeans_2.fit_transform(player_mat_2_t)
# cluster_labels_2 = kmeans_2.labels_
# player_info_2['cluster'] = cluster_labels_2
# player_info_2['cluster'].replace([0,1,2], [3,4,5], inplace=True)
#
# player_info_2.to_csv('~/capstone_project/data/t_sne_test.csv')
#
#
# player_mat_3 = featurized_data[featurized_data['player_id'].isin(big_cluster_3)]
# player_info_3 = player_mat_3[['player_id','display_name']]
# player_mat_3.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
# player_mat_3.fillna(0, inplace = True)
# player_mat_3 = scale(player_mat_3)
#
#
#
# t_sne_3 = TSNE(n_components = 9)
# player_mat_3_t = t_sne_1.fit_transform(player_mat_3)
# player_mat_3_t = scale(player_mat_3_t)
#
# kmeans_3 = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
# precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
# kmeans_3.fit_transform(player_mat_3_t)
# cluster_labels_3 = kmeans_3.labels_
# player_info_3['cluster'] = cluster_labels_3
#player_info_3['cluster'].replace([0,1,2,3], [6,7,8,9], inplace=True)

# #group the cluster_dfs
# t_sne_clusters = pd.concat([player_info_1, player_info_2, player_info_3])
# t_sne_clusters.to_csv('~/capstone_project/data/t_sne_clusters.csv')
