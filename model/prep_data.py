#feature creation and scaling the data for the model

'''
player_id
age #current age
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
include = ['player_id','age','season_exp','catch_shoot_freq','attempt_at_rim_2',
'attempt_cut_run_2','attempt_drive_2','attempt_jumper_2','attempt_jumper_3',
'attempt_off_dribble_2','attempt_off_dribble_3','attempt_post_2','made_at_rim_2',
'made_cut_run_2','made_drive_2','made_jumper_2','made_jumper_3','made_off_dribble_2',
'made_off_dribble_3','made_post_2','ast','blk','blk_a','dreb','fta','ftm','gp',
'min_game','oreb','pf','pfd','reb','stl','tov','c_dreb_game','c_oreb_game',
'avg_speed_def','avg_speed_off','avg_speed_tot','mi_game_def','mi_game_off',
'd_fga_paint','d_fga_perim','d_fgm_paint','d_fgm_perim','d_ppm_paint','d_ppm_perim','pass_total']


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

ast_min = (ast*gp)/min_tot
blk_min = (blk*gp)/min_tot
blk_a_min = (blk_a*gp)/min_tot
dreb_min = (dreb*gp)/min_tot
oreb_min = (oreb*gp)/min_tot
fta_min = (fta*gp)/min_tot
ftm_min = (ftm*gp)/min_tot
stl_min = (ftl*gp)/min_tot
tov_min = (tov*gp)/min_tot
c_dreb_min = (c_dreb_game*gp)/min_tot
c_dreb_min = (c_oreb_game*gp)/min_tot
d_fga_paint_min = (d_fga_paint*gp)/min_tot
d_fga_perim_min = (d_fga_perim*gp)/min_tot
d_fgm_paint_min = (d_fgm_paint*gp)/min_tot
d_fgm_perim_min = (d_fgm_perim*gp)/min_tot
mi_def_min = (mi_game_def*gp)/min_tot
mi_def_min = (mi_game_off*gp)/min_tot


#...and drop these
drp = ['attempt_at_rim_2','attempt_cut_run_2','attempt_drive_2','attempt_jumper_2',
'attempt_jumper_3','attempt_off_dribble_2','attempt_off_dribble_3','attempt_post_2',
'made_at_rim_2','made_cut_run_2','made_drive_2','made_jumper_2','made_jumper_3',
'made_off_dribble_2','made_off_dribble_3','made_post_2','ast','blk','dreb','oreb',
'fta','ftm','stl','tov','c_dreb_game','c_oreb_game','d_fga_paint','d_fga_perim',
'd_fgm_paint','d_fgm_perim','mi_game_def','mi_game_off']




if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    player_data = pd.read_csv('~/capstone_project/data/aggregated_player_data.csv')
