from __future__ import division
import pandas as pd

######################################
#read in the yearly player data that should be merged
raw_data_2016_17 = pd.read_csv('~/capstone_project/data/raw_player_data_16_17.csv')
raw_data_2015_16 = pd.read_csv('~/capstone_project/data/raw_player_data_15_16.csv')
raw_data_2014_15 = pd.read_csv('~/capstone_project/data/raw_player_data_14_15.csv')
raw_data_2013_14 = pd.read_csv('~/capstone_project/data/raw_player_data_13_14.csv')

raw_data_dfs = [raw_data_2016_17,raw_data_2015_16, raw_data_2014_15, raw_data_2013_14,]
#####################################

def format_data(raw_data_dfs):
    '''
    INPUT: takes in a list of raw data dfs, each representing a season's worth of data
    OUTPUT: generates file of aggregated, cleaned, and featurized data.  Also returns a df of same
    '''

    include = ['player_id','display_name','min_game','total_made','pos',
    'attempt_RA','attempt_paint','attempt_corner_3','attempt_non_corner_3','attempt_mid',
    'ast','blk','dreb_pos','fta','gp','oreb_pos','stl','tov',
    'd_fga_mid','d_fga_overall','d_fga_paint','d_fga_perim','d_fga_threes']

    #try to get this one again: 'ast_shot_made',

    lst_of_dfs = []

    #iterate over dfs. for each, create new cols required for aggregation and drop unnecessary cols.
    #add each cleaned df to a list
    for file in raw_data_dfs:
        file.fillna(0, inplace = True)
        data = file[include]
        data['min_tot'] = data['gp'] * data['min_game']
        data['ast_tot'] = data['ast'] * data['gp']
        data['blk_tot'] = data['blk'] * data['gp']
        data['fta_tot'] = data['fta'] * data['gp']
        data['stl_tot'] = data['stl'] * data['gp']
        data['tov_tot'] = data['tov'] * data['gp']
        data['d_fga_mid_tot'] = data['d_fga_mid'] * data['gp']
        data['d_fga_overall_tot'] = data['d_fga_overall'] * data['gp']
        data['d_fga_paint_tot'] = data['d_fga_paint'] * data['gp']
        data['d_fga_perim_tot'] = data['d_fga_perim'] * data['gp']
        data['d_fga_threes_tot'] = data['d_fga_threes'] * data['gp']
        drop_cols = ['min_game','ast','blk','dreb','oreb','stl','tov',
                     'fta','d_fga_mid','d_fga_overall','d_fga_paint',
                     'd_fga_perim','d_fga_threes']
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
    player_data['blk_min'] = player_data['blk_tot']/player_data['min_tot']
    player_data['fta_pos'] = player_data['fta_tot']/player_data['pos']
    player_data['stl_min'] = player_data['stl_tot']/player_data['min_tot']
    player_data['d_fga_paint_pct'] = player_data['d_fga_paint_tot']/player_data['d_fga_overall_tot']
    player_data['d_fga_perim_pct'] = player_data['d_fga_perim_tot']/player_data['d_fga_overall_tot']
    player_data['d_fga_threes_pct'] = player_data['d_fga_threes_tot']/player_data['d_fga_overall_tot']
    player_data['d_fga_mid_pct'] = player_data['d_fga_mid_tot']/player_data['d_fga_overall_tot']

    drp = ['total_made','attempt_RA','attempt_paint',
        'attempt_corner_3','attempt_non_corner_3','attempt_mid','ast_tot','blk_tot','fta_tot',
        'stl_tot','tov_tot','pos','d_fga_mid_tot','d_fga_overall_tot','d_fga_paint_tot',
        'd_fga_perim_tot','d_fga_threes_tot']

        # try to get this one again: 'ast_shot_made'

    #clean the aggregated dataframe, push to csv and return a df
    player_data.drop(drp, inplace = True, axis = 1)
    player_data.fillna(0, inplace = True)
    player_data.to_csv('~/capstone_project/data/featurized_data.csv')
    return player_data

if __name__ == '__main___':
    player_data = format_data(raw_data_dfs)
