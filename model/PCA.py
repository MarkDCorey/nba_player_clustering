from sklearn import decomposition, cluster, datasets,ensemble, manifold, random_projection, preprocessing, metrics,mixture
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet,fcluster,maxdists,leaves_list
from scipy.spatial.distance import pdist, squareform
from mpl_toolkits.mplot3d import Axes3D



featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
player_mat = preprocessing.scale(player_mat)


# pca = decomposition.PCA(n_components=11) #, whiten=True
# fit_pca = pca.fit_transform(player_mat)
# reduced_data = preprocessing.scale(fit_pca)



# kmeans = cluster.KMeans(n_clusters=10, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
#         precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
# kmeans.fit_transform(player_mat)
# cluster_labels = kmeans.labels_
# player_info['cluster'] = cluster_labels
# player_info.to_csv('~/capstone_project/data/clustered_players.csv')

#
#
# clf = mixture.GMM(7, n_iter = 500, random_state = 3).fit(player_mat)
#
# clusters = clf.predict(player_mat)
# player_info['cluster'] = clusters
#
#
# Z = linkage(player_mat, method = 'ward', metric = 'euclidean')
# clusters_h = fcluster(Z, 7, criterion='maxclust')


# pca = decomposition.PCA(n_components=2)
# X_r = pca.fit(player_mat).transform(player_mat)
# target_names = ['cluster_1','cluster_2','cluster_3','cluster_4', 'cluster_5','cluster_6','cluster_7']
#
#
# # Percentage of variance explained for each components
# print('explained variance ratio (first two components): %s'
#       % str(pca.explained_variance_ratio_))
#
# plt.figure()
# colors = ['navy', 'turquoise', 'darkorange','blue','green','red','cyan']
# lw = 2
#
# for color, i, target_name in zip(colors, [0,1,2,3,4,5,6], target_names):
#     plt.scatter(X_r[clusters == i, 0], X_r[clusters == i, 1], color=color, alpha=.8, lw=lw,
#                 label=target_name)
# plt.legend(loc='best', shadow=False, scatterpoints=1)
# plt.title('PCA')
#
#
# plt.show()


fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
X_reduced = decomposition.PCA(n_components=3).fit_transform(player_mat)
ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2]) 
    # c=clusters_h,cmap=plt.cm.Paired)
ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])

ax.set_xlim3d(-5, 7)
ax.set_ylim3d(-5,6)
ax.set_zlim3d(-4,4)

plt.show()




# Xred, evals, evecs = dim_red_pca(SN,2)
#
# xlab = '1. PC - ExpVar = {:.2f} %'.format(evals[0]/sum(evals)*100) # determine variance portion
# ylab = '2. PC - ExpVar = {:.2f} %'.format(evals[1]/sum(evals)*100)
# # plot the clusters, each set separately
# plt.figure()
# ax = plt.gca()
# scatterHs = []
# clr = ['r', 'b', 'k']
# for cluster in set(labels_):
#     scatterHs.append(ax.scatter(Xred[labels_ == cluster, 0], Xred[labels_ == cluster, 1],
#                    color=clr[cluster], label='Cluster {}'.format(cluster)))
# plt.legend(handles=scatterHs,loc=4)
# plt.setp(ax, title='First and Second Principle Components', xlabel=xlab, ylabel=ylab)
# # plot also the eigenvectors for deriving the influence of each feature
# fig, ax = plt.subplots(2,1)
# ax[0].bar([1, 2, 3, 4],evecs[0])
# plt.setp(ax[0], title="First and Second Component's Eigenvectors ", ylabel='Weight')
# ax[1].bar([1, 2, 3, 4],evecs[1])
# plt.setp(ax[1], xlabel='Features', ylabel='Weight')



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


# def scree_plot(num_components, pca):
#     ind = np.arange(num_components)
#     vals = pca.explained_variance_ratio_
#     plt.figure(figsize=(12, 12), dpi=300)
#     ax = plt.subplot(111)
#     ax.bar(ind, vals)
#
#     #tick labels take a fontsize = arg
#     # ax.set_xticklabels(ind)
#     ax.set_yticklabels(('0.00', '0.05', '0.10', '0.15', '0.20', '0.25','0.30','0.35','0.40'))
#     ax.set_ylim(0, .5)
#     # ax.set_xlim(0-0.45, 15+0.45)
#
#     ax.set_xlabel("Principal Component", fontsize=6)
#     ax.set_ylabel("Variance Explained", fontsize=6)
#
#     plt.title("PCA", fontsize=12)
#     plt.savefig("scree.png", dpi= 300)
#     plt.show()

# pca = decomposition.PCA(n_components=15).fit(player_mat) #, whiten=True

# scree_plot(15, pca)
#
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
#
#
# def plot_embedding(X, y, title=None):
#     x_min, x_max = np.min(X, 0), np.max(X, 0)
#     X = (X - x_min) / (x_max - x_min)
#     plt.figure(figsize=(10, 6), dpi=250)
#     ax = plt.subplot(111)
#     ax.axis('off')
#     ax.patch.set_visible(False)
#     for i in range(X.shape[0]):
#         plt.text(X[i, 0], X[i, 1], str(digits.target[i]), color=plt.cm.Set1(y[i] / 10.), fontdict={'weight': 'bold', 'size': 12})
#
#     plt.xticks([]), plt.yticks([])
#     plt.ylim([-0.1,1.1])
#     plt.xlim([-0.1,1.1])
#
#     if title is not None:
#         plt.title(title, fontsize=16)


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
