import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler,normalize




if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
    test = featurized_data[featurized_data.min_game >10]
    test_players = test[['player_id','display_name']]
    test.drop(['player_id','display_name','Unnamed: 0'], inplace = True, axis = 1)
    #,'age','height','weight','season_exp','min_game'
    test.fillna(0, inplace = True)
    X = normalize(test)


    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))
