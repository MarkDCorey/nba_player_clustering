from scipy.cluster.hierarchy import linkage, dendrogram, cophenet,fcluster,maxdists,leaves_list
from sklearn import decomposition, datasets,ensemble, manifold, random_projection, metrics
from scipy.spatial.distance import pdist, squareform
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler,normalize,scale


def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Truncated Dendrogram', fontsize = 14)
        plt.xlabel('Cluster size', fontsize = 12)
        plt.ylabel('Distance', fontsize = 12)
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata



featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
# player_mat = normalize(player_mat)
player_mat = normalize(player_mat)

pca = decomposition.PCA(n_components=15) #, whiten=True
player_mat = pca.fit_transform(player_mat)
player_mat = normalize(player_mat)


Z = linkage(player_mat, method = 'ward')#, metric = 'euclidean')

c,coph_dists = cophenet(Z, pdist(player_mat))
#
#
# # getting clusters...
max_d = 100
k=3
clusters = fcluster(Z, k, criterion='maxclust')
# # clusters = fcluster(Z, max_d, criterion='distance')

player_info['cluster'] = clusters
player_info.to_csv('~/capstone_project/data/big_clusters.csv')

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
Z_1 = linkage(player_mat_1, method = 'ward')#, metric = 'euclidean')
c_1,coph_dists_1 = cophenet(Z_1, pdist(player_mat_1))
# #use 12 PCs
#3 or 5 clusters
max_d_1 = 5
clusters_1 = fcluster(Z_1, max_d_1, criterion='distance')
player_info_1['cluster'] = clusters_1


plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index', fontsize = 14)
plt.ylabel('Distance', fontsize = 20)
dendrogram(
    Z_1,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.savefig("full_dendrogram_1.png", dpi= 300)
plt.title('cluster_1')
plt.show()

fancy_dendrogram(
    Z_1,
    truncate_mode='lastp',
    p=12,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,
    # max_d=max_d,  # plot a horizontal cut-off line
)
plt.savefig("trunc_dendrogram_1.png", dpi= 300)
plt.show()


player_mat_2 = featurized_data[featurized_data['player_id'].isin(big_cluster_2)]
player_info_2 = player_mat_2[['player_id','display_name']]
player_mat_2.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat_2.fillna(0, inplace = True)
player_mat_2 = normalize(player_mat_2)
pca_2 = decomposition.PCA(n_components=12)
pca_2_fit = pca_2.fit_transform(player_mat_2)
player_mat_2 = normalize(pca_2_fit)
Z_2 = linkage(player_mat_2, method = 'ward')#, metric = 'euclidean')
c_2,coph_dists_2 = cophenet(Z_2, pdist(player_mat_2))
# # #use 12 PCs
#maybe 3 clusters
max_d_2 = 5
clusters_2 = fcluster(Z_2, max_d_2, criterion='distance')
player_info_2['cluster'] = clusters_2
player_info_2['cluster'].replace([1,2,3], [4,5,6], inplace=True)

plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index', fontsize = 14)
plt.ylabel('Distance', fontsize = 20)
dendrogram(
    Z_2,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.savefig("full_dendrogram_2.png", dpi= 300)
plt.title('cluster_2')
plt.show()

fancy_dendrogram(
    Z_2,
    truncate_mode='lastp',
    p=12,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,
    # max_d=max_d,  # plot a horizontal cut-off line
)
plt.savefig("trunc_dendrogram_2.png", dpi= 300)
plt.show()


#
player_mat_3 = featurized_data[featurized_data['player_id'].isin(big_cluster_3)]
player_info_3 = player_mat_3[['player_id','display_name']]
player_mat_3.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat_3.fillna(0, inplace = True)
player_mat_3 = normalize(player_mat_3)
pca_3 = decomposition.PCA(n_components=12)
pca_3_fit = pca_3.fit_transform(player_mat_3)
player_mat_3 = normalize(pca_3_fit)
Z_3 = linkage(player_mat_3, method = 'ward')#, metric = 'euclidean')
c_3,coph_dists_3 = cophenet(Z_3, pdist(player_mat_3))
# #use 12 PCs
# #appear to be 5 clusters
max_d_3 = 6
clusters_3 = fcluster(Z_3, max_d_3, criterion='distance')
player_info_3['cluster'] = clusters_3
player_info_3['cluster'].replace([1,2,3,4], [7,8,9,10], inplace=True)


plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index', fontsize = 14)
plt.ylabel('Distance', fontsize = 20)
dendrogram(
    Z_3,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.savefig("full_dendrogram_3.png", dpi= 300)
plt.title('cluster_3')
plt.show()

fancy_dendrogram(
    Z_3,
    truncate_mode='lastp',
    p=12,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,
    # max_d=max_d,  # plot a horizontal cut-off line
)
plt.savefig("trunc_dendrogram_3.png", dpi= 300)
plt.show()



# calculate the inertia
def sum_squared_dist(mat, cent):
    lst_of_dist = []
    for i in range(mat.shape[0]):
        dist = np.linalg.norm(mat.as_matrix()[i,:] -  cent)
        lst_of_dist.append(dist)
    sum_of_dist = sum(lst_of_dist)
    return sum_of_dist


player_mat_1_df = pd.DataFrame(player_mat_1)
player_info_1.reset_index(inplace = True)
player_mat_1_df['cluster'] = player_info_1['cluster']
mat_1_1 = player_mat_1_df[player_mat_1_df.cluster == 1]
mat_1_1.drop('cluster', inplace = True, axis = 1)
mat_1_2 = player_mat_1_df[player_mat_1_df.cluster == 2]
mat_1_2.drop('cluster', inplace = True, axis = 1)
mat_1_3 = player_mat_1_df[player_mat_1_df.cluster == 3]
mat_1_3.drop('cluster', inplace = True, axis = 1)
cent_1_1 = np.mean(mat_1_1.as_matrix()[:,:], axis=0)
cent_1_2 = np.mean(mat_1_2.as_matrix()[:,:], axis=0)
cent_1_3 = np.mean(mat_1_3.as_matrix()[:,:], axis=0)
dist_1_1 = sum_squared_dist(mat_1_1, cent_1_1)
dist_1_2 = sum_squared_dist(mat_1_2, cent_1_2)
dist_1_3 = sum_squared_dist(mat_1_3, cent_1_3)
inertia_mat_1 = dist_1_1 + dist_1_2 + dist_1_3


player_mat_2_df = pd.DataFrame(player_mat_2)
player_info_2.reset_index(inplace = True)
player_mat_2_df['cluster'] = player_info_2['cluster']
mat_2_4 = player_mat_2_df[player_mat_2_df.cluster == 4]
mat_2_4.drop('cluster', inplace = True, axis = 1)
mat_2_5= player_mat_2_df[player_mat_2_df.cluster == 5]
mat_2_5.drop('cluster', inplace = True, axis = 1)
mat_2_6 = player_mat_2_df[player_mat_2_df.cluster == 6]
mat_2_6.drop('cluster', inplace = True, axis = 1)
cent_2_4 = np.mean(mat_2_4.as_matrix()[:,:], axis=0)
cent_2_5 = np.mean(mat_2_5.as_matrix()[:,:], axis=0)
cent_2_6 = np.mean(mat_2_6.as_matrix()[:,:], axis=0)
dist_2_4 = sum_squared_dist(mat_2_4, cent_2_4)
dist_2_5 = sum_squared_dist(mat_2_5, cent_2_5)
dist_2_6 = sum_squared_dist(mat_2_6, cent_2_6)
inertia_mat_2 = dist_2_4 + dist_2_5 + dist_2_6


player_mat_3_df = pd.DataFrame(player_mat_3)
player_info_3.reset_index(inplace = True)
player_mat_3_df['cluster'] = player_info_3['cluster']
mat_3_7 = player_mat_3_df[player_mat_3_df.cluster == 7]
mat_3_7.drop('cluster', inplace = True, axis = 1)
mat_3_8= player_mat_3_df[player_mat_3_df.cluster == 8]
mat_3_8.drop('cluster', inplace = True, axis = 1)
mat_3_9 = player_mat_3_df[player_mat_3_df.cluster == 9]
mat_3_9.drop('cluster', inplace = True, axis = 1)
mat_3_10 = player_mat_3_df[player_mat_3_df.cluster == 10]
mat_3_10.drop('cluster', inplace = True, axis = 1)
cent_3_7 = np.mean(mat_3_7.as_matrix()[:,:], axis=0)
cent_3_8 = np.mean(mat_3_8.as_matrix()[:,:], axis=0)
cent_3_9 = np.mean(mat_3_9.as_matrix()[:,:], axis=0)
cent_3_10 = np.mean(mat_3_10.as_matrix()[:,:], axis=0)
dist_3_7 = sum_squared_dist(mat_3_7, cent_3_7)
dist_3_8 = sum_squared_dist(mat_3_8, cent_3_8)
dist_3_9 = sum_squared_dist(mat_3_9, cent_3_9)
dist_3_10 = sum_squared_dist(mat_3_10, cent_3_10)
inertia_mat_3 = dist_3_7 + dist_3_8 + dist_3_9 + dist_3_10

#group the cluster_dfs
final_clusters = pd.concat([player_info_1, player_info_2, player_info_3])
composite_clusters = final_clusters.to_csv('~/capstone_project/data/composite_clusters.csv')






'''
code to get PCA graphs for each of the major clusters
'''
# pca_3 = decomposition.PCA(n_components=15)
# pca_3_fit = pca_3.fit_transform(player_mat_3)
#
# var_ex = pca_3.explained_variance_ratio_
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
# plt.savefig("PCA_3.png", dpi= 300)
#
#
# plt.show()




# player_info.to_csv('~/capstone_project/data/clustered_composite.csv')
