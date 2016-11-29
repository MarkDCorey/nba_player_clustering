import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler,normalize,scale
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE


big_clusters = pd.read_csv('~/capstone_project/data/big_clusters.csv')
clusters = big_clusters['cluster'].tolist()

featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
# player_mat = normalize(player_mat)
player_mat = normalize(player_mat)

pca = decomposition.PCA(n_components=8) #, whiten=True
player_mat = pca.fit_transform(player_mat)

# kmeans_3 = KMeans(n_clusters=10, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
# precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
# kmeans_3.fit_transform(player_mat)
# cluster_labels_3 = kmeans_3.labels_


fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
# X_reduced = decomposition.PCA(n_components=3).fit_transform(player_mat)
RS = 1223456
X_reduced = TSNE(random_state=RS, n_components = 3).fit_transform(player_mat)
ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=clusters,cmap=plt.cm.Paired)

ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])

# ax.set_xlim3d(0, 4)
# ax.set_ylim3d(0,2)
# ax.set_zlim3d(0,3)

plt.show()
