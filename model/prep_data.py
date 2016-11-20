from __future__ import division
import pandas as pd


#read in data to df
player_data = pd.read_csv('~/capstone_project/data/aggregated_player_data_15_16.csv')
player_data.fillna(0, inplace = True)

#reduce the df
include = ['player_id','display_name','min_game','total_made','ast_shot_made','pos',
'attempt_RA','attempt_paint','attempt_corner_3','attempt_non_corner_3','attempt_mid',
'ast','blk','dreb','fta','gp','oreb','stl','tov',
'd_freq_paint','d_freq_perim','d_freq_mid','d_freq_threes']

#removed age, catch_shoot_freq,'avg_speed_def','avg_speed_off',,'d_ppm_overall','d_ppm_paint','d_ppm_perim',

player_data_rd = player_data[include]
#
# #add 'min_tot' to new df
player_data_rd['min_tot'] = player_data_rd['gp'] * player_data_rd['min_game']

#for shots, volume and efficiency are probably the most relevant


player_data_rd['attempt_RA_pos'] = player_data_rd['attempt_RA']/player_data_rd['pos']
player_data_rd['attempt_paint_pos'] = player_data_rd['attempt_paint']/player_data_rd['pos']
player_data_rd['attempt_corner_3_pos'] = player_data_rd['attempt_corner_3']/player_data_rd['pos']
player_data_rd['attempt_non_corner_3_pos'] = player_data_rd['attempt_non_corner_3']/player_data_rd['pos']
player_data_rd['attempt_mid_pos'] = player_data_rd['attempt_mid']/player_data_rd['pos']

player_data_rd['ast_shot_pct'] = player_data_rd['ast_shot_made']/player_data_rd['total_made']


# player_data_rd['attempt_at_rim_2_min'] = player_data_rd['attempt_at_rim_2']/player_data_rd['min_tot']
# player_data_rd['attempt_cut_run_2_min'] = player_data_rd['attempt_cut_run_2']/player_data_rd['min_tot']
# player_data_rd['attempt_drive_2_min'] = player_data_rd['attempt_drive_2']/player_data_rd['min_tot']
# player_data_rd['attempt_jumper_2_min'] = player_data_rd['attempt_jumper_2']/player_data_rd['min_tot']
# player_data_rd['attempt_jumper_3_min'] = player_data_rd['attempt_jumper_3']/player_data_rd['min_tot']
# player_data_rd['attempt_off_dribble_2_min'] = player_data_rd['attempt_off_dribble_2']/player_data_rd['min_tot']
# player_data_rd['attempt_off_dribble_3_min'] = player_data_rd['attempt_off_dribble_3']/player_data_rd['min_tot']
# player_data_rd['attempt_post_2_min'] = player_data_rd['attempt_post_2']/player_data_rd['min_tot']
# player_data_rd['made_at_rim_2_min'] = player_data_rd['made_at_rim_2']/player_data_rd['min_tot']
# player_data_rd['made_cut_run_2_min'] = player_data_rd['made_cut_run_2']/player_data_rd['min_tot']
# player_data_rd['made_drive_2_min'] = player_data_rd['made_drive_2']/player_data_rd['min_tot']
# player_data_rd['made_jumper_2_min'] = player_data_rd['made_jumper_2']/player_data_rd['min_tot']
# player_data_rd['made_jumper_3_min'] = player_data_rd['made_jumper_3']/player_data_rd['min_tot']
# player_data_rd['made_off_dribble_2_min'] = player_data_rd['made_off_dribble_2']/player_data_rd['min_tot']
# player_data_rd['made_off_dribble_3_min'] = player_data_rd['made_off_dribble_3']/player_data_rd['min_tot']
# player_data_rd['made_post_2_min'] = player_data_rd['made_post_2']/player_data_rd['min_tot']
# player_data_rd['eff_at_rim_2'] = (player_data_rd['made_at_rim_2']/player_data_rd['attempt_at_rim_2'])
# player_data_rd['eff_cut_run_2'] = player_data_rd['made_cut_run_2']/player_data_rd['attempt_cut_run_2']
# player_data_rd['eff_drive_2'] = player_data_rd['made_drive_2']/player_data_rd['attempt_drive_2'] #if player_data_rd['attempt_drive_2'] > 10 else 0.
# player_data_rd['eff_jumper_2'] = player_data_rd['made_jumper_2']/player_data_rd['attempt_jumper_2'] #if player_data_rd['attempt_jumper_2'] > 10 else 0.
# player_data_rd['eff_jumper_3'] = player_data_rd['made_jumper_3']/player_data_rd['attempt_jumper_3'] #if player_data_rd['attempt_jumper_3'] > 10 else 0.
# player_data_rd['eff_off_dribble_2'] = player_data_rd['made_off_dribble_2']/player_data_rd['attempt_off_dribble_2'] #if player_data_rd['attempt_off_dribble_2'] > 10 else 0.
# player_data_rd['eff_off_dribble_3'] = player_data_rd['made_off_dribble_3']/player_data_rd['attempt_off_dribble_3'] #if player_data_rd['attempt_off_dribble_3'] > 10 else 0.
# player_data_rd['eff_post_2'] = player_data_rd['made_post_2']/player_data_rd['attempt_post_2'] #if player_data_rd['attempt_post_2'] > 10 else 0.

#standardizing to per min
player_data_rd['ast_pos'] = (player_data_rd['ast']*player_data_rd['gp'])/player_data_rd['pos']
player_data_rd['blk_min'] = (player_data_rd['blk']*player_data_rd['gp'])/player_data_rd['min_tot']
# player_data_rd['blk_a_min'] = (player_data_rd['blk_a']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['dreb_min'] = (player_data_rd['dreb']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['oreb_pos'] = (player_data_rd['oreb']*player_data_rd['gp'])/player_data_rd['pos']
#removed ftm per min and added ft efficiency in its place
player_data_rd['fta_pos'] = (player_data_rd['fta']*player_data_rd['gp'])/player_data_rd['pos']
player_data_rd['stl_min'] = (player_data_rd['stl']*player_data_rd['gp'])/player_data_rd['min_tot']

#ft efficiency
# player_data_rd['eff_ft'] = player_data_rd['ftm']/player_data_rd['fta']

#ast/turnover efficiency
# player_data_rd['ast_tov'] = player_data_rd['ast']/player_data_rd['tov']

#use contested rb as a separate feature to reb.  is this redundant
# player_data_rd['c_dreb_min'] = (player_data_rd['c_dreb_game']*player_data_rd['gp'])/player_data_rd['min_tot']
# player_data_rd['c_oreb_min'] = (player_data_rd['c_oreb_game']*player_data_rd['gp'])/player_data_rd['min_tot']

#d_fga useful to determine how often they are guarding the ball per min
# player_data_rd['d_fga_paint_min'] = (player_data_rd['d_fga_paint']*player_data_rd['gp'])/player_data_rd['min_tot']
# player_data_rd['d_fga_perim_min'] = (player_data_rd['d_fga_perim']*player_data_rd['gp'])/player_data_rd['min_tot']
# player_data_rd['d_fga_mid_min'] = (player_data_rd['d_fga_mid']*player_data_rd['gp'])/player_data_rd['min_tot']
# player_data_rd['d_fga_threes_min'] = (player_data_rd['d_fga_threes']*player_data_rd['gp'])/player_data_rd['min_tot']

#efficiency for each
# player_data_rd['d_eff_paint'] = player_data_rd['d_fgm_paint']/player_data_rd['d_fga_paint']
# player_data_rd['d_eff_perim'] = player_data_rd['d_fgm_perim']/player_data_rd['d_fga_perim']
# player_data_rd['d_eff_mid'] = player_data_rd['d_fgm_mid']/player_data_rd['d_fga_mid']
# player_data_rd['d_eff_threes'] = player_data_rd['d_fgm_threes']/player_data_rd['d_fga_threes']

#how much ground they are covering per min on off and def
# player_data_rd['mi_def_min'] = (player_data_rd['mi_game_def']*player_data_rd['gp'])/player_data_rd['min_tot']
# player_data_rd['mi_off_min'] = (player_data_rd['mi_game_off']*player_data_rd['gp'])/player_data_rd['min_tot']

#passes per min
# player_data_rd['pass_min']= player_data_rd['pass_total']/player_data_rd['min_tot']


#...and drop these
drp = ['min_game','total_made','ast_shot_made','attempt_RA','attempt_paint',
'attempt_corner_3','attempt_non_corner_3','attempt_mid','ast','blk','dreb','fta',
'gp','oreb','stl','tov','pos','total_made']



# #remember to check for null and 0 values
#     #some records are missing height and weight (0 as placeholder)

player_data_rd.drop(drp, inplace = True, axis = 1)
player_data_rd.to_csv('~/capstone_project/data/featurized_data.csv')
