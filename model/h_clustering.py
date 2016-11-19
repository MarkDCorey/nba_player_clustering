from scipy.cluster.hierarchy import linkage, dendrogram, cophenet,fcluster
from scipy.spatial.distance import pdist
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler,normalize,scale
from sklearn.decomposition import NMF




featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
test = featurized_data[featurized_data.min_tot >800]
# test = test[test.player_id != 203937]
# test = test[test.player_id != 203948]
# test = test[test.player_id != 202355]
test_players = test[['player_id','display_name']]
test.drop(['Unnamed: 0','player_id','display_name','mi_def_min','mi_off_min','pass_min','season_exp','min_game','min_tot'], inplace = True, axis = 1)


off_cols = ['attempt_at_rim_2_min', 'attempt_cut_run_2_min',
                'attempt_drive_2_min', 'attempt_jumper_2_min',
                'attempt_jumper_3_min', 'attempt_off_dribble_2_min',
                'attempt_off_dribble_3_min', 'attempt_post_2_min', 'eff_at_rim_2',
                'eff_cut_run_2', 'eff_drive_2', 'eff_jumper_2', 'eff_jumper_3',
                'eff_off_dribble_2', 'eff_off_dribble_3', 'eff_post_2', 'ast_min',
                'oreb_min', 'fta_min', 'tov_min','eff_ft', 'ast_tov', 'c_oreb_min']

def_cols = ['blk_min', 'blk_a_min','dreb_min','stl_min','c_dreb_min','d_fga_paint_min', 'd_fga_perim_min',
    'd_fga_mid_min','d_fga_threes_min', 'd_eff_paint', 'd_eff_perim', 'd_eff_mid','d_eff_threes']


shooting_cols = ['attempt_at_rim_2_min', 'attempt_cut_run_2_min',
                'attempt_drive_2_min', 'attempt_jumper_2_min',
                'attempt_jumper_3_min', 'attempt_off_dribble_2_min',
                'attempt_off_dribble_3_min', 'attempt_post_2_min', 'eff_at_rim_2',
                'eff_cut_run_2', 'eff_drive_2', 'eff_jumper_2', 'eff_jumper_3',
                'eff_off_dribble_2', 'eff_off_dribble_3', 'eff_post_2']



test = test[def_cols]
features = test.columns
test_players.set_index('player_id',inplace = True, drop = True)
test.fillna(0, inplace = True)
test = normalize(test)


nmf = NMF(n_components=7)
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
test = normalize(players_by_topic)



# Z = linkage(test, method = 'ward', metric = 'euclidean' )
#
# c,coph_dists = cophenet(Z, pdist(test))
#
#
# # getting clusters...
# # max_d = 50
# # clusters = fcluster(Z, max_d, criterion='distance')
# # clusters
#
# #alternatively...
# k=10
# clusters = fcluster(Z, k, criterion='maxclust')
#
# test_players['cluster'] = clusters




# # calculate full dendrogram
# plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dendrogram(
#     Z,
#     leaf_rotation=90.,  # rotates the x axis labels
#     leaf_font_size=8.,  # font size for the x axis labels
# )
# plt.show()



# plt.title('Hierarchical Clustering Dendrogram (truncated)')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dendrogram(
#     Z,
#     truncate_mode='lastp',  # show only the last p merged clusters
#     p=12,  # show only the last p merged clusters
#     show_leaf_counts=False,  # otherwise numbers in brackets are counts
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,  # to get a distribution impression in truncated branches
# )
# plt.show()


#
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
#
#
#
#
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
