from sklearn import decomposition, cluster, datasets,ensemble, manifold, random_projection, preprocessing, metrics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet,fcluster,maxdists,leaves_list
from scipy.spatial.distance import pdist, squareform



featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >500]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
player_mat = preprocessing.scale(player_mat)


pca = decomposition.PCA(n_components=15) #, whiten=True
fit_pca = pca.fit_transform(player_mat)


# reduced_data = normalize(reduced_data)

# Z = linkage(player_mat, method = 'ward', metric = 'euclidean')
#
# max_d = 100
# k=12
# clusters = fcluster(Z, k, criterion='maxclust')
# # clusters = fcluster(Z, max_d, criterion='distance')
#
#
# player_info['cluster'] = clusters
# # player_info.to_csv('~/capstone_project/data/clustered_players.csv')


def scree_plot(num_components, pca):
    ind = np.arange(num_components)
    vals = pca.explained_variance_ratio_
    plt.figure(figsize=(12, 12), dpi=300)
    ax = plt.subplot(111)
    ax.bar(ind, vals)

    #tick labels take a fontsize = arg
    # ax.set_xticklabels(ind)
    ax.set_yticklabels(('0.00', '0.05', '0.10', '0.15', '0.20', '0.25','0.30','0.35','0.40'))
    ax.set_ylim(0, .5)
    # ax.set_xlim(0-0.45, 15+0.45)

    ax.set_xlabel("Principal Component", fontsize=6)
    ax.set_ylabel("Variance Explained", fontsize=6)

    plt.title("PCA", fontsize=12)
    plt.savefig("scree.png", dpi= 300)
    plt.show()


# scree_plot(15, pca)


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


def plot_embedding(X, y, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)
    plt.figure(figsize=(10, 6), dpi=250)
    ax = plt.subplot(111)
    ax.axis('off')
    ax.patch.set_visible(False)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(digits.target[i]), color=plt.cm.Set1(y[i] / 10.), fontdict={'weight': 'bold', 'size': 12})

    plt.xticks([]), plt.yticks([])
    plt.ylim([-0.1,1.1])
    plt.xlim([-0.1,1.1])

    if title is not None:
        plt.title(title, fontsize=16)


# plot_embedding(fit_pca, digits.target)


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




# # calculate full dendrogram
# plt.figure(figsize=(25, 10))
# # plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dendrogram(
#     Z,
#     leaf_rotation=90.,  # rotates the x axis labels
#     leaf_font_size=8.,  # font size for the x axis labels
# )
# plt.show()

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
# def fancy_dendrogram(*args, **kwargs):
#     max_d = kwargs.pop('max_d', None)
#     if max_d and 'color_threshold' not in kwargs:
#         kwargs['color_threshold'] = max_d
#     annotate_above = kwargs.pop('annotate_above', 0)
#
#     ddata = dendrogram(*args, **kwargs)
#
#     if not kwargs.get('no_plot', False):
#         plt.title('Hierarchical Clustering Dendrogram (truncated)')
#         plt.xlabel('sample index or (cluster size)')
#         plt.ylabel('distance')
#         for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
#             x = 0.5 * sum(i[1:3])
#             y = d[1]
#             if y > annotate_above:
#                 plt.plot(x, y, 'o', c=c)
#                 plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
#                              textcoords='offset points',
#                              va='top', ha='center')
#         if max_d:
#             plt.axhline(y=max_d, c='k')
#     return ddata
# #
# #
# #
# #
# fancy_dendrogram(
#     Z,
#     truncate_mode='lastp',
#     p=12,
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,
#     annotate_above=10,
#     max_d=max_d,  # plot a horizontal cut-off line
# )
# plt.show()


# scores = []
#
# # k_vals = [6,8,9,10,11,12,13,14,15]
#
# kmeans = KMeans(n_clusters=7, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
#         precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
# kmeans.fit(reduced_data)
# labels = kmeans.labels_
# s_score = silhouette_score(reduced_data, labels, metric='euclidean',sample_size=None)
#
# labels_df = pd.DataFrame(labels)
# c_counts = labels_df[0].value_counts()
# c_dist = [round(clust/float(sum(c_counts)),2) for clust in c_counts]
# player_info_off['cluster'] = labels
