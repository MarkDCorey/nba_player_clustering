import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler,normalize,scale
from sklearn.decomposition import NMF




if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
    test = featurized_data[featurized_data.min_game >10]
    test_players = test[['player_id','display_name']]
    test.drop(['Unnamed: 0','player_id','display_name','mi_def_min','mi_off_min','pass_min','season_exp','min_game','min_tot'], inplace = True, axis = 1)
    features = test.columns
    test_players.set_index('player_id',inplace = True, drop = True)
    test.fillna(0, inplace = True)
    test = normalize(test)

    #
    nmf = NMF(n_components=20)
    W_sklearn = nmf.fit_transform(test)
    H_sklearn = nmf.components_
    W = pd.DataFrame(W_sklearn)
    H = pd.DataFrame(H_sklearn)
    W.set_index(test_players.index,inplace = True, drop = True)
    H.columns = features
    players_by_topic = pd.concat([test_players,W],axis=1)
    features_by_topic = H

    players_by_topic.reset_index(inplace=True)
    player_info = players_by_topic[['player_id', 'display_name']]
    players_by_topic.drop(['player_id','display_name'], inplace = True, axis = 1)
    players_by_topic = normalize(players_by_topic)

    #

    db = DBSCAN(eps=0.001, min_samples=10).fit(players_by_topic)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # # Number of clusters in labels, ignoring noise if present.
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # print('Estimated number of clusters: %d' % n_clusters_)
    # print("Silhouette Coefficient: %0.3f"
    #   % metrics.silhouette_score(X, labels))
