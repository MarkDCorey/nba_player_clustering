from __future__ import division
import pandas as pd


def format_data(raw_data_dfs):
    '''
    INPUT: takes in a list of raw data dfs, each representing a season's worth of data
    OUTPUT: generates file of aggregated, cleaned, and featurized data.  Also returns a df of same
    '''

    include = ['player_id','display_name','min_game','pos',
    'attempt_RA','attempt_paint','attempt_corner_3','attempt_non_corner_3','attempt_mid',
    'ast','blk_pos','dreb_pos','fta','gp','oreb_pos','stl_pos',
    'd_fga_overall','d_fga_paint','d_fga_threes','ast_shot_made',
    'made_RA','made_corner_3','made_mid','made_non_corner_3','made_paint']


    lst_of_dfs = []

    #iterate over dfs. for each, create new cols required for aggregation and drop unnecessary cols.
    #add each cleaned df to a list
    for df in raw_data_dfs:
        df.fillna(0, inplace = True)
        data = df[include]
        data['total_made'] = data['made_RA'] + data['made_corner_3'] + data['made_mid'] \
            + data['made_non_corner_3'] + data['made_paint']
        data['min_tot'] = data['gp'] * data['min_game']
        data['ast_tot'] = data['ast'] * data['gp']
        data['fta_tot'] = data['fta'] * data['gp']
        data['d_fga_overall_tot'] = data['d_fga_overall'] * data['gp']
        data['d_fga_paint_tot'] = data['d_fga_paint'] * data['gp']
        data['d_fga_threes_tot'] = data['d_fga_threes'] * data['gp']
        data['d_fga_mid_tot'] = data['d_fga_overall_tot'] - data['d_fga_paint_tot'] - data['d_fga_threes_tot']

        drop_cols = ['min_game','ast',
                     'fta','d_fga_overall','d_fga_paint',
                     'd_fga_threes','made_RA','made_corner_3','made_mid','made_non_corner_3','made_paint']
        data.drop(drop_cols, inplace = True, axis = 1)
        lst_of_dfs.append(data)

    #merged the cleaned dfs
    merged_data = lst_of_dfs[0]
    for i, df in enumerate(lst_of_dfs):
        if i > 0:
            merged_data = merged_data.append(df, ignore_index= True)

    #group data in the merged file and sum each numeric column.
    #create new features and drop the unnecessary remaining columns
    merged_data = merged_data.groupby(['player_id','display_name']).sum()
    player_data = merged_data
    player_data['attempt_RA_pos'] = player_data['attempt_RA']/player_data['pos']
    player_data['attempt_paint_pos'] = player_data['attempt_paint']/player_data['pos']
    player_data['attempt_corner_3_pos'] = player_data['attempt_corner_3']/player_data['pos']
    player_data['attempt_non_corner_3_pos'] = player_data['attempt_non_corner_3']/player_data['pos']
    player_data['attempt_mid_pos'] = player_data['attempt_mid']/player_data['pos']
    player_data['ast_shot_pct'] = player_data['ast_shot_made']/player_data['total_made']
    player_data['ast_pos'] = player_data['ast_tot']/player_data['pos']
    player_data['fta_pos'] = player_data['fta_tot']/player_data['pos']
    player_data['d_fga_paint_pct'] = player_data['d_fga_paint_tot']/player_data['d_fga_overall_tot']
    player_data['d_fga_threes_pct'] = player_data['d_fga_threes_tot']/player_data['d_fga_overall_tot']
    player_data['d_fga_mid_pct'] = player_data['d_fga_mid_tot']/player_data['d_fga_overall_tot']

    drp = ['attempt_RA','attempt_paint',
        'attempt_corner_3','attempt_non_corner_3','attempt_mid','ast_tot','fta_tot',
        'pos','d_fga_mid_tot','d_fga_overall_tot','d_fga_paint_tot',
        'd_fga_threes_tot','ast_shot_made','total_made']


    #clean the aggregated dataframe, push to csv and return a df
    player_data.drop(drp, inplace = True, axis = 1)
    player_data.fillna(0, inplace = True)
    player_data.to_csv('~/capstone_project/data/featurized_data.csv')
    return player_data

if __name__ == '__main__':
    raw_data_2016_17 = pd.read_csv('~/capstone_project/data/raw_player_data_16_17.csv')
    raw_data_2015_16 = pd.read_csv('~/capstone_project/data/raw_player_data_15_16.csv')
    raw_data_2014_15 = pd.read_csv('~/capstone_project/data/raw_player_data_14_15.csv')
    raw_data_2013_14 = pd.read_csv('~/capstone_project/data/raw_player_data_13_14.csv')
    raw_data_dfs = [raw_data_2016_17,raw_data_2015_16, raw_data_2014_15, raw_data_2013_14]
    player_data = format_data(raw_data_dfs)
