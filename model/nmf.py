from sklearn.decomposition import NMF
from sklearn.preprocessing import scale, normalize
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans


featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
test = featurized_data[featurized_data.min_game >10]
test_players = test[['player_id','display_name']]
test.drop(['Unnamed: 0','player_id','display_name'], inplace = True, axis = 1)
features = test.columns
test_players.set_index('player_id',inplace = True, drop = True)
test.fillna(0, inplace = True)
test = normalize(test)

scores = []
n_comp = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]
for i in n_comp:
    nmf = NMF(n_components=i)
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


    k_vals = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    inertia_list = []

    for j in k_vals:
        KMeans_test = KMeans(n_clusters=j, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
        precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
        KMeans_test.fit(players_by_topic)
        test_labels = KMeans_test.labels_
        players_clustered = pd.DataFrame(players_by_topic)
        players_clustered['cluster'] = test_labels
        players_clustered['player_name'] = player_info['display_name']
        s_score = silhouette_score(players_by_topic, test_labels, metric='euclidean',sample_size=None)

        inertia_list.append(KMeans_test.inertia_)
        # print 'n_comp: ',i
        # print 'k_val: ',j
        # print 's_score: ',s_score
        # print 'inertia: ',KMeans_test.inertia_

        temp = {'n_comp':i,'k_val':j,'inertia':KMeans_test.inertia_,'s_score':s_score}
        scores.append(temp)

score_df = pd.DataFrame(scores)

    # plt.plot(k_vals, inertia_list)
    # plt.xlabel('k')
    # plt.ylabel('sum of error')
    # plt.show()
