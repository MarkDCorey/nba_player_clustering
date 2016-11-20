from sklearn.decomposition import PCA
from sklearn.preprocessing import scale,normalize,StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >2000]
player_info_off = player_mat[['player_id','display_name']]
player_info_def= player_mat[['player_id','display_name']]
player_mat.drop(['Unnamed: 0','player_id','display_name','mi_def_min','mi_off_min','pass_min','season_exp','min_game','min_tot'], inplace = True, axis = 1)


shooting_cols = ['attempt_at_rim_2_min', 'attempt_cut_run_2_min',
                'attempt_drive_2_min', 'attempt_jumper_2_min',
                'attempt_jumper_3_min', 'attempt_off_dribble_2_min',
                'attempt_off_dribble_3_min', 'attempt_post_2_min', 'eff_at_rim_2',
                'eff_cut_run_2', 'eff_drive_2', 'eff_jumper_2', 'eff_jumper_3',
                'eff_off_dribble_2', 'eff_off_dribble_3', 'eff_post_2', 'ast_min',
                'oreb_min', 'fta_min', 'tov_min','eff_ft', 'ast_tov', 'c_oreb_min']

def_cols = ['blk_min', 'blk_a_min','dreb_min','stl_min','c_dreb_min','d_fga_paint_min', 'd_fga_perim_min',
    'd_fga_mid_min','d_fga_threes_min', 'd_eff_paint', 'd_eff_perim', 'd_eff_mid','d_eff_threes']


off_cols = ['attempt_at_rim_2_min', 'attempt_cut_run_2_min',
                'attempt_drive_2_min', 'attempt_jumper_2_min',
                'attempt_jumper_3_min', 'attempt_off_dribble_2_min',
                'attempt_off_dribble_3_min', 'attempt_post_2_min', 'eff_at_rim_2',
                'eff_cut_run_2', 'eff_drive_2', 'eff_jumper_2', 'eff_jumper_3',
                'eff_off_dribble_2', 'eff_off_dribble_3', 'eff_post_2']


#create two feature mats
player_mat_off = player_mat[off_cols]
player_info_off.set_index(player_info_off.player_id,inplace = True, drop = True)
features_off = player_mat_off.columns

player_mat_def = player_mat[def_cols]
player_info_def.set_index(player_info_def.player_id,inplace = True, drop = True)
features_def = player_mat_def.columns


#prep each for algos
player_mat_off.fillna(0, inplace = True)
player_mat_off = scale(player_mat_off)

player_mat_def.fillna(0, inplace = True)
player_mat_def = scale(player_mat_def)



reduced_data = PCA(n_components=10, whiten=True).fit_transform(player_mat_off)
# reduced_data = normalize(reduced_data)

scores = []

# k_vals = [6,8,9,10,11,12,13,14,15]

kmeans = KMeans(n_clusters=7, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
        precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
kmeans.fit(reduced_data)
labels = kmeans.labels_
s_score = silhouette_score(reduced_data, labels, metric='euclidean',sample_size=None)

labels_df = pd.DataFrame(labels)
c_counts = labels_df[0].value_counts()
c_dist = [round(clust/float(sum(c_counts)),2) for clust in c_counts]
player_info_off['cluster'] = labels
