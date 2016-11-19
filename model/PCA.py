from sklearn.decomposition import PCA
from sklearn.preprocessing import scale,normalize,StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
test = featurized_data[featurized_data.min_game >10]
test_players = test[['player_id','display_name']]
test.drop(['Unnamed: 0','player_id','display_name','mi_def_min','mi_off_min','pass_min','season_exp','min_game','min_tot'], inplace = True, axis = 1)
features = test.columns
test_players.set_index('player_id',inplace = True, drop = True)
test.fillna(0, inplace = True)
test = normalize(test)


# # X = df.as_matrix() #take data out of dataframe
# X = scale(X) #standardize the data before giving it to the PCA.
# #I standardize the data because some features such as PF or steals have lower magnitudes than other features such as FG2A
# #I want both to contribute equally to the PCA, so I make sure they're on the same scale.

# pca = PCA(n_components=8) #great PCA object
# pca.fit(test) #pull out principle components
# var_expl = pca.explained_variance_ratio_ #find amount of variance explained by each component
# tot_var_expl = np.array([sum(var_expl[0:i+1]) for i,x in enumerate(var_expl)]) #create vector with cumulative variance
#
# plt.figure(figsize=(12,4)) #create cumulative proportion of variance plot
# plt.subplot(1,2,1)
# plt.plot(range(1,len(tot_var_expl)+1), tot_var_expl*100,'o-')
# plt.axis([0, len(tot_var_expl)+1, 0, 100])
# plt.xlabel('Number of PCA Components Included')
# plt.ylabel('Percentage of variance explained (%)')
#
# plt.subplot(1,2,2) #create scree plot
# plt.plot(range(1,len(var_expl)+1), var_expl*100,'o-')
# plt.axis([0, len(var_expl)+1, 0, 100])
# plt.xlabel('PCA Component');


reduced_data = PCA(n_components=14, whiten=False).fit_transform(test)

scores = []

k_vals = [6,8,9,10,11,12,13,14,15]


# for j in xrange(10):
KMeans_test = KMeans(n_clusters=5, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
KMeans_test.fit(reduced_data)
test_labels = KMeans_test.labels_
#     players_clustered = pd.DataFrame(players_by_topic)
#     players_clustered['cluster'] = test_labels
#     players_clustered['player_name'] = player_info['display_name']
#     players_clustered['player_id'] = player_info['player_id']
#     s_score = silhouette_score(players_by_topic, test_labels, metric='euclidean',sample_size=None)
#
#         # inertia_list.append(KMeans_test.inertia_)
#         # print 'n_comp: ',i
#         # print 'k_val: ',j
#         # print 's_score: ',s_score
#         # print 'inertia: ',KMeans_test.inertia_
#
#     temp = {'n_comp':i,'k_val':j,'avg_inertia':KMeans_test.inertia_/j,'s_score':s_score}
#     scores.append(temp)
#
# score_df = pd.DataFrame(scores)
