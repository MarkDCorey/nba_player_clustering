from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale, normalize,StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
test = featurized_data[featurized_data.min_game >10]
test_players = test[['player_id','display_name']]
test.drop(['Unnamed: 0','player_id','display_name'], inplace = True, axis = 1)
features = featurized_data.columns
test_players.set_index('player_id',inplace = True, drop = True)
test.fillna(0, inplace = True)
test = normalize(test)

count_topics = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]

lda = LDA(n_topics=4, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

lda.fit(test)


# for i in [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]:
#     KMeans_test = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
#     precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
#     KMeans_test.fit(players_by_topic)
#     test_labels = KMeans_test.labels_
#     players_clustered = pd.DataFrame(players_by_topic)
#     players_clustered['cluster'] = test_labels
#     players_clustered['player_name'] = player_info['display_name']
#     score = silhouette_score(players_by_topic, test_labels, metric='euclidean',sample_size=None)
#     print score
