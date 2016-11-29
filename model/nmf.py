from __future__ import division
from sklearn.decomposition import NMF
from sklearn.preprocessing import scale, normalize
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans


featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['Unnamed: 0','player_id','display_name','min_tot'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
player_mat = normalize(player_mat)


#different combos to test
n_comps = [2,3,4,5,6,7,8,9,10]
k_vals = [6,7,8,9,10,11,12,13,14,15]

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


# scores = test_reduction_clustering_combos(n_comps, k_vals, player_mat, player_info)



    # plt.plot(k_vals, inertia_list)
    # plt.xlabel('k')
    # plt.ylabel('sum of error')
    # plt.show()



def test_composite(n_comps, k_vals, mat_off, mat_def, player_info_off, player_info_def):
    '''
    tests different latent feature counts for offensive and defensive mat inputs

    '''
    scores = []
    counter = 0

    for i in n_comps:
        nmf = NMF(n_components=i)
        W_off = nmf.fit_transform(mat_off)
        H_off = nmf.components_
        W_off_df = pd.DataFrame(W_off)
        W_off_df.columns = [str(c)+'.Off' for c in W_off_df.columns]
        H_off_df = pd.DataFrame(H_off)
        W_off_df.set_index(player_info_off.index,inplace = True, drop = True)
        H_off_df.columns = pd.DataFrame(mat_off).columns
        players_by_topic_off = pd.concat([player_info_off,W_off_df],axis=1)
        features_by_topic_off = H_off_df

        for j in n_comps:
            nmf = NMF(n_components=j)
            W_def = nmf.fit_transform(mat_def)
            H_def = nmf.components_
            W_def_df = pd.DataFrame(W_def)
            W_def_df.columns = [str(c)+'.Def' for c in W_def_df.columns]
            H_def_df = pd.DataFrame(H_def)
            W_def_df.set_index(player_info_def.index,inplace = True, drop = True)
            H_def_df.columns = pd.DataFrame(mat_def).columns
            players_by_topic_def = pd.concat([player_info_def,W_def_df],axis=1)
            players_by_topic_def.drop(['player_id','display_name'], inplace = True, axis = 1)
            features_by_topic_def = H_def_df


            merged_df = pd.concat([players_by_topic_off,players_by_topic_def],axis=1)
            merged_df_player_info = merged_df[['player_id','display_name']]
            merged_df.drop(['player_id','display_name'], inplace = True, axis = 1)

            for k in k_vals:
                kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
                precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
                kmeans.fit(merged_df)
                labels = kmeans.labels_
                s_score = silhouette_score(merged_df, labels, metric='euclidean',sample_size=None)

                labels = pd.DataFrame(labels)
                c_counts = labels[0].value_counts()
                c_dist = [round(clust/float(sum(c_counts)),2) for clust in c_counts]


                temp = {'off_comp':i, 'def_comp':j, 'k_val':k, 'inertia': kmeans.inertia_,
                 's_score':s_score, 'cluster_dist': c_dist}

                scores.append(temp)

    scores_df = pd.DataFrame(scores)
    merged_df['cluster'] = labels

    return scores_df, merged_df






def get_clusters_merged(n_comps_off, n_comps_def,k_val, mat_off, mat_def, player_info_off, player_info_def):
    '''
    tests different latent feature counts for offensive and defensive mat inputs

    '''
    scores = []
    counter = 0


    nmf = NMF(n_components=n_comps_off)
    W_off = nmf.fit_transform(mat_off)
    H_off = nmf.components_
    W_off_df = pd.DataFrame(W_off)
    W_off_df.columns = [str(c)+'.Off' for c in W_off_df.columns]
    H_off_df = pd.DataFrame(H_off)
    W_off_df.set_index(player_info_off.index,inplace = True, drop = True)
    H_off_df.columns = pd.DataFrame(mat_off).columns
    players_by_topic_off = pd.concat([player_info_off,W_off_df],axis=1)
    features_by_topic_off = H_off_df

    nmf = NMF(n_components=n_comps_def)
    W_def = nmf.fit_transform(mat_def)
    H_def = nmf.components_
    W_def_df = pd.DataFrame(W_def)
    W_def_df.columns = [str(c)+'.Def' for c in W_def_df.columns]
    H_def_df = pd.DataFrame(H_def)
    W_def_df.set_index(player_info_def.index,inplace = True, drop = True)
    H_def_df.columns = pd.DataFrame(mat_def).columns
    players_by_topic_def = pd.concat([player_info_def,W_def_df],axis=1)
    players_by_topic_def.drop(['player_id','display_name'], inplace = True, axis = 1)
    features_by_topic_def = H_def_df

    merged_df = pd.concat([players_by_topic_off,players_by_topic_def],axis=1)
    merged_df_player_info = merged_df[['player_id','display_name']]
    merged_df.drop(['player_id','display_name'], inplace = True, axis = 1)

    kmeans = KMeans(n_clusters=k_val, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
    precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
    kmeans.fit(merged_df)
    labels = kmeans.labels_
    s_score = silhouette_score(merged_df, labels, metric='euclidean',sample_size=None)

    labels_df = pd.DataFrame(labels)
    c_counts = labels_df[0].value_counts()
    c_dist = [round(clust/float(sum(c_counts)),2) for clust in c_counts]


    temp = {'off_comp':n_comps_off, 'def_comp':n_comps_def, 'k_val':k_val, 'inertia': kmeans.inertia_,
         's_score':s_score, 'cluster_dist': c_dist}

    scores.append(temp)

    scores_df = pd.DataFrame(scores)
    merged_df = pd.DataFrame(merged_df)
    merged_df.set_index(merged_df_player_info['player_id'], inplace = True)
    merged_df['cluster'] = labels
    merged_df = pd.concat([merged_df_player_info,merged_df],axis=1)
    merged_df.drop('player_id', axis=1, inplace=True)

    return scores_df, merged_df

# scores_df, merged_df = get_clusters_merged(4,4,10, player_mat_off, player_mat_def, player_info_off, player_info_def)

def get_clusters(n_comps,k_val,mat,player_info):
    '''
    tests different latent feature counts for offensive and defensive mat inputs

    '''
    scores = []
    counter = 0


    nmf = NMF(n_components=n_comps)
    W = nmf.fit_transform(mat)
    H = nmf.components_
    W_df = pd.DataFrame(W)
    H_df = pd.DataFrame(H)
    W_df.set_index(player_info.index,inplace = True, drop = True)
    H_df.columns = pd.DataFrame(mat).columns
    players_by_topic = pd.concat([player_info,W_df],axis=1)
    features_by_topic = H_df
    features_by_topic.columns = H_df.columns
    W = scale(W)


    kmeans = KMeans(n_clusters=k_val, init='k-means++', n_init=10, max_iter=300, tol=0.0001, \
    precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto')
    kmeans.fit(W)
    labels = kmeans.labels_
    s_score = silhouette_score(W, labels, metric='euclidean',sample_size=None)

    labels_df = pd.DataFrame(labels)
    c_counts = labels_df[0].value_counts()
    c_dist = [round(clust/float(sum(c_counts)),2) for clust in c_counts]


    temp = {'n_comps':n_comps, 'k_val':k_val, 'inertia': kmeans.inertia_,
         's_score':s_score, 'cluster_dist': c_dist}

    scores.append(temp)

    scores_df = pd.DataFrame(scores)
    players_by_topic['cluster'] = labels
    players_by_topic.drop('player_id',axis=1,inplace=True)
    # merged_df.set_index(merged_df_player_info['player_id'], inplace = True)
    #

    return players_by_topic, features_by_topic


players_by_topic, features_by_topic = get_clusters(4,11, player_mat, player_info)
