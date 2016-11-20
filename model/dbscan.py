import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler,normalize,scale
from sklearn.decomposition import NMF




featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['Unnamed: 0','player_id','display_name','min_tot'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
player_mat = scale(player_mat)

db = DBSCAN(eps=0.5, min_samples=5).fit(player_mat)
# core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # # Number of clusters in labels, ignoring noise if present.
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # print('Estimated number of clusters: %d' % n_clusters_)
    # print("Silhouette Coefficient: %0.3f"
    #   % metrics.silhouette_score(X, labels))
