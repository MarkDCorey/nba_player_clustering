from scipy.cluster.hierarchy import linkage, dendrogram, cophenet,fcluster,maxdists,leaves_list
from sklearn import decomposition, datasets,ensemble, manifold, random_projection, metrics
from scipy.spatial.distance import pdist, squareform
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler,normalize,scale

big_clusters = pd.read_csv('~/capstone_project/data/big_clusters.csv')

big_cluster_1 = big_clusters['player_id'][big_clusters.cluster == 1].tolist()
big_cluster_2 = big_clusters['player_id'][big_clusters.cluster == 2].tolist()
big_cluster_3 = big_clusters['player_id'][big_clusters.cluster == 3].tolist()

#



featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
player_mat = normalize(player_mat)

pca = decomposition.PCA(n_components=8) #, whiten=True
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
clusters

player_info['cluster'] = clusters
player_info.to_csv('~/capstone_project/data/clustered_players.csv')


# fig = plt.figure(figsize = (8,8))
#
# plt.plot(range(1, len(Z)+1),Z[::-1, 2])
# knee = np.diff(Z[::-1, 2], 2)
# plt.plot(range(2, len(Z)), knee)
# plt.title='Screeplot'
# plt.xlabel='partition',
# plt.ylabel='cluster distance'
#
# plt.tight_layout()
# plt.show()




# calculate full dendrogram
plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index', fontsize = 14)
plt.ylabel('Distance', fontsize = 20)
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.savefig("full_dendrogram.png", dpi= 300)
plt.show()
#
#
#
# # plt.title('Hierarchical Clustering Dendrogram (truncated)')
# # plt.xlabel('sample index')
# # plt.ylabel('distance')
# # dendrogram(
# #     Z,
# #     truncate_mode='lastp',  # show only the last p merged clusters
# #     p=12,  # show only the last p merged clusters
# #     show_leaf_counts=False,  # otherwise numbers in brackets are counts
# #     leaf_rotation=90.,
# #     leaf_font_size=12.,
# #     show_contracted=True,  # to get a distribution impression in truncated branches
# # )
# # plt.show()
#
#
# #
# plt.title('Hierarchical Clustering Dendrogram (truncated)')
# plt.xlabel('sample index or (cluster size)')
# plt.ylabel('distance')
# dendrogram(
#     Z,
#     truncate_mode='lastp',  # show only the last p merged clusters
#     p=10,  # show only the last p merged clusters
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,  # to get a distribution impression in truncated branches
# )
# plt.show()
#
#
#
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
#
#
#
#
fancy_dendrogram(
    Z,
    truncate_mode='lastp',
    p=12,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,
    max_d=max_d,  # plot a horizontal cut-off line
)
plt.savefig("trunc_dendrogram.png", dpi= 300)
plt.show()
