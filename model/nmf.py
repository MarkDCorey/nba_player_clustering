from __future__ import division
from sklearn.decomposition import NMF
from sklearn.preprocessing import scale, normalize
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans


featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >800]
player_info_off = player_mat[['player_id','display_name']]
player_info_def= player_mat[['player_id','display_name']]
player_mat.drop(['Unnamed: 0','player_id','display_name','mi_def_min','mi_off_min','pass_min','season_exp','min_game','min_tot'], inplace = True, axis = 1)


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


#create two feature mats
player_mat_off = player_mat[off_cols]
player_info_off.set_index(player_info_off.player_id,inplace = True, drop = True)
features_off = player_mat_off.columns

player_mat_def = player_mat[off_cols]
player_info_def.set_index(player_info_def.player_id,inplace = True, drop = True)
features_def = player_mat_def.columns


#prep each for algos
player_mat_off.fillna(0, inplace = True)
player_mat_off = normalize(player_mat_off)

player_mat_def.fillna(0, inplace = True)
player_mat_def = normalize(player_mat_off)

#different combos to test
n_comps = [2,3,4,5,6,7,8,9,10]
k_vals = [2,4,5,6,7,8,9,10,11,12,13,14,15]

def test_reduction_clustering_combos(n_comps, k_vals, mat, player_info):
    '''
    takes in list of n_comps for nmf and k_vals for kmeans
    produces scores for each combo
    '''
    scores = []

    for i in n_comps:
        nmf = NMF(n_components=i)
        W = nmf.fit_transform(mat)
        H = nmf.components_
        W_df = pd.DataFrame(W)
        H_df = pd.DataFrame(H)
        W_df.set_index(player_info.index,inplace = True, drop = True)
        H_df.columns = pd.DataFrame(mat).columns
        players_by_topic = pd.concat([player_info,W_df],axis=1)
        features_by_topic = H_df



        for j in k_vals:
            KMeans_test = KMeans(n_clusters=j, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
            precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
            KMeans_test.fit(W)
            test_labels = KMeans_test.labels_
            s_score = silhouette_score(W, test_labels, metric='euclidean',sample_size=None)

            print 'n_comp: ',i
            print 'k_val: ',j
            print 's_score: ',s_score
            print 'inertia: ',KMeans_test.inertia_
            print ""

            temp = {'n_comp':i,'k_val':j,'inertia':KMeans_test.inertia_,'s_score':s_score}
            scores.append(temp)

    score_df = pd.DataFrame(scores)
    return score_df


# scores = test_reduction_clustering_combos(n_comps, k_vals, player_mat_def, player_info_def)

    # plt.plot(k_vals, inertia_list)
    # plt.xlabel('k')
    # plt.ylabel('sum of error')
    # plt.show()



def test_composite(n_comps, k_vals, mat_off, mat_def, player_info_off, player_info_def):
    '''
    tests different latent feature counts for offensive and defensive mat inputs

    '''
    scores = []

    for i in n_comps:
        nmf = NMF(n_components=i)
        W_off = nmf.fit_transform(mat_off)
        H_off = nmf.components_
        W_off_df = pd.DataFrame(W_off)
        W_off_df.columns = [str(i)+'.Off' for i in W_off_df.columns]
        H_off_df = pd.DataFrame(H_off)
        W_off_df.set_index(player_info_off.index,inplace = True, drop = True)
        H_off_df.columns = pd.DataFrame(mat_off).columns
        players_by_topic_off = pd.concat([player_info_off,W_off_df],axis=1)
        features_by_topic_off = H_off_df

        for i in n_comps:
            nmf = NMF(n_components=i)
            W_def = nmf.fit_transform(mat_def)
            H_def = nmf.components_
            W_def_df = pd.DataFrame(W_def)
            W_def_df.columns = [str(i)+'.Def' for i in W_def_df.columns]
            H_def_df = pd.DataFrame(H_def)
            W_def_df.set_index(player_info_def.index,inplace = True, drop = True)
            H_def_df.columns = pd.DataFrame(mat_def).columns
            players_by_topic_def = pd.concat([player_info_def,W_def_df],axis=1)
            players_by_topic_def.drop(['player_id','display_name'], inplace = True, axis = 1)
            features_by_topic_def = H_def_df


            merged_feats = pd.concat([players_by_topic_off,players_by_topic_def],axis=1)
    return merged_feats


test = test_composite(n_comps, k_vals, player_mat_off, player_mat_def, player_info_off, player_info_def)
