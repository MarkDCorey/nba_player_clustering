from __future__ import division
import pandas as pd


#feature creation and scaling the data for the model
'''
player_id
age #current age
height #inches
weight #pounds
display_name
dleague_flag
first_name
last_name
position
roster_status
season_exp #number of completed seasons
team_id
team_name

#all shot data in totals for season
attempt_2
attempt_3
attempt_at_rim_2
attempt_cut_run_2
attempt_drive_2
attempt_jumper_2
attempt_jumper_3
attempt_off_dribble_2
attempt_off_dribble_3
attempt_post_2
made_2
made_3
made_at_rim_2
made_cut_run_2
made_drive_2
made_jumper_2
made_jumper_3
made_off_dribble_2
made_off_dribble_3
made_post_2
total_attempt
total_made

#for year
catch_shoot_freq

#all stats other than gp are per game (for year)
ast
blk
blk_a
dreb
fta
ftm
gp #for season
min_game #avg for season
oreb
pf
pfd
reb
stl
tov

#contested rbs per game (for year)
c_dreb_game
c_oreb_game

#avg speed overall (for year)
avg_speed_def
avg_speed_off
avg_speed_tot

#miles per game (for year)
mi_game_def
mi_game_off
mi_game_tot


#the paint/perim/overalls are averages per game
#the pct plus minus is overall and refers to the differene in defense relative to
#league average.  Lower is better (fg % allowed compared to league average)

d_fga_overall
d_fga_paint
d_fga_perim
d_fgm_overall
d_fgm_paint
d_fgm_perim
d_ppm_overall
d_ppm_paint
d_ppm_perim

#total passes for season
pass_total
'''

#read in data to df
player_data = pd.read_csv('~/capstone_project/data/aggregated_player_data.csv')

#reduce the df
include = ['player_id','display_name','age','height','weight','season_exp','catch_shoot_freq',
'attempt_at_rim_2','attempt_cut_run_2','attempt_drive_2','attempt_jumper_2','attempt_jumper_3',
'attempt_off_dribble_2','attempt_off_dribble_3','attempt_post_2','made_at_rim_2',
'made_cut_run_2','made_drive_2','made_jumper_2','made_jumper_3','made_off_dribble_2',
'made_off_dribble_3','made_post_2','ast','blk','blk_a','dreb','fta','ftm','gp',
'min_game','oreb','pf','pfd','reb','stl','tov','c_dreb_game','c_oreb_game',
'avg_speed_def','avg_speed_off','mi_game_def','mi_game_off','d_fga_paint','d_fga_perim',
'd_fgm_paint','d_fgm_perim','d_ppm_paint','d_ppm_perim','pass_total']


player_data_red = player_data[include]

#add 'min_tot' to new df
player_data_rd['min_tot'] = player_data_rd['gp'] * player_data_rd['min_game']

#then add these...
player_data_rd['attempt_at_rim_2_min'] = player_data_rd['attempt_at_rim_2']/player_data_rd['min_tot']
player_data_rd['attempt_cut_run_2_min'] = player_data_rd['attempt_cut_run_2']/player_data_rd['min_tot']
player_data_rd['attempt_drive_2_min'] = player_data_rd['attempt_drive_2']/player_data_rd['min_tot']
player_data_rd['attempt_jumper_2_min'] = player_data_rd['attempt_jumper_2']/player_data_rd['min_tot']
player_data_rd['attempt_jumper_3_min'] = player_data_rd['attempt_jumper_3']/player_data_rd['min_tot']
player_data_rd['attempt_off_dribble_2_min'] = player_data_rd['attempt_off_dribble_2']/player_data_rd['min_tot']
player_data_rd['attempt_off_dribble_3_min'] = player_data_rd['attempt_off_dribble_3']/player_data_rd['min_tot']
player_data_rd['attempt_post_2_min'] = player_data_rd['attempt_post_2']/player_data_rd['min_tot']
player_data_rd['made_at_rim_2_min'] = player_data_rd['made_at_rim_2']/player_data_rd['min_tot']
player_data_rd['made_cut_run_2_min'] = player_data_rd['made_cut_run_2']/player_data_rd['min_tot']
player_data_rd['made_drive_2_min'] = player_data_rd['made_drive_2']/player_data_rd['min_tot']
player_data_rd['made_jumper_2_min'] = player_data_rd['made_jumper_2']/player_data_rd['min_tot']
player_data_rd['made_jumper_3_min'] = player_data_rd['made_jumper_3']/player_data_rd['min_tot']
player_data_rd['made_off_dribble_2_min'] = player_data_rd['made_off_dribble_2']/player_data_rd['min_tot']
player_data_rd['made_off_dribble_3_min'] = player_data_rd['made_off_dribble_3']/player_data_rd['min_tot']
player_data_rd['made_post_2_min'] = player_data_rd['made_post_2']/player_data_rd['min_tot']

player_data_rd['ast_min'] = (player_data_rd['ast']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['blk_min'] = (player_data_rd['blk']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['blk_a_min'] = (player_data_rd['blk_a']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['reb_min'] = (player_data_rd['reb']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['oreb_min'] = (player_data_rd['oreb']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['fta_min'] = (player_data_rd['fta']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['ftm_min'] = (player_data_rd['ftm']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['stl_min'] = (player_data_rd['ftl']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['tov_min'] = (player_data_rd['tov']*player_data_rd['gp'])/player_data_rd['min_tot']

player_data_rd['c_dreb_min'] = (player_data_rd['c_dreb_game']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['c_dreb_min'] = (player_data_rd['c_oreb_game']*player_data_rd['gp'])/player_data_rd['min_tot']

player_data_rd['d_fga_paint_min'] = (player_data_rd['d_fga_paint']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['d_fga_perim_min'] = (player_data_rd['d_fga_perim']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['d_fgm_paint_min'] = (player_data_rd['d_fgm_paint']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['d_fgm_perim_min'] = (player_data_rd['d_fgm_perim']*player_data_rd['gp'])/player_data_rd['min_tot']

player_data_rd['mi_def_min'] = (player['mi_game_def']*player_data_rd['gp'])/player_data_rd['min_tot']
player_data_rd['mi_def_min'] = (player_data_rd['mi_game_off']*player['gp'])/player_data_rd['min_tot']

player_data_rd['pass_min']= player_data_rd['pass_total']/player_data_rd['min_tot']


#...and drop these
drp = ['attempt_at_rim_2','attempt_cut_run_2','attempt_drive_2','attempt_jumper_2',
'attempt_jumper_3','attempt_off_dribble_2','attempt_off_dribble_3','attempt_post_2',
'made_at_rim_2','made_cut_run_2','made_drive_2','made_jumper_2','made_jumper_3',
'made_off_dribble_2','made_off_dribble_3','made_post_2','ast','blk','dreb','oreb',
'fta','ftm','stl','tov','c_dreb_game','c_oreb_game','d_fga_paint','d_fga_perim',
'd_fgm_paint','d_fgm_perim','mi_game_def','mi_game_off','pass_total']


#remember to check for null and 0 values
    #some records are missing height and weight (0 as placeholder)


player_data_rd.drop(drp, inplace = True)
player_data_rd.to_csv('~/capstone_project/data/featurized_data.csv')