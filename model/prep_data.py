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
include = [player_id,age,season_exp,catch_shoot_freq,attempt_at_rim_2,
attempt_cut_run_2,attempt_drive_2,attempt_jumper_2,attempt_jumper_3,
attempt_off_dribble_2,attempt_off_dribble_3,attempt_post_2,made_at_rim_2,
made_cut_run_2,made_drive_2,made_jumper_2,made_jumper_3,made_off_dribble_2,
made_off_dribble_3,made_post_2,ast,blk,blk_a,dreb,fta,ftm,gp,min_game,oreb,
pf,pfd,reb,stl,tov,c_dreb_game,c_oreb_game,avg_speed_def,avg_speed_off,
avg_speed_tot, mi_game_def,mi_game_off,d_fga_paint,d_fga_perim,d_fgm_paint,
d_fgm_perim,d_ppm_paint,d_ppm_perim,pass_total]


player_data_red = player_data[include]

#add 'min_tot' to new df
player_data_rd['min_tot'] = player_data_rd['gp'] * player_data_rd['min_game']


#then add these...
attempt_at_rim_2_min = attempt_at_rim_2/min_tot
attempt_cut_run_2_min = attempt_cut_run_2/min_tot
attempt_drive_2_min = attempt_drive_2/min_tot
attempt_jumper_2_min = attempt_jumper_2/min_tot
attempt_jumper_3_min = attempt_jumper_3/min_tot
attempt_off_dribble_2_min = attempt_off_dribble_2/min_tot
attempt_off_dribble_3_min = attempt_off_dribble_3/min_tot
attempt_post_2_min = attempt_post_2/min_tot
made_at_rim_2_min = made_at_rim_2/min_tot
made_cut_run_2_min = made_cut_run_2/min_tot
made_drive_2_min = made_drive_2/min_tot
made_jumper_2_min = made_jumper_2/min_tot
made_jumper_3_min = made_jumper_3/min_tot
made_off_dribble_2_min = made_off_dribble_2/min_tot
made_off_dribble_3_min = made_off_dribble_3/min_tot
made_post_2_min = made_post_2/min_tot

ast_min = (ast*gp)/min_tot
blk_min = (blk*gp)/min_tot
blk_a_min = (blk_a*gp)/min_tot

dreb
oreb
fta
ftm
stl
tov
c_dreb_game
c_oreb_game
d_fga_paint
d_fga_perim
d_fgm_paint
d_fgm_perim
d_ppm_paint
d_ppm_perim

#...and drop these
ast


attempt_at_rim_2
attempt_cut_run_2
attempt_drive_2
attempt_jumper_2
attempt_jumper_3
attempt_off_dribble_2
attempt_off_dribble_3
attempt_post_2

made_at_rim_2
made_cut_run_2
made_drive_2
made_jumper_2
made_jumper_3
made_off_dribble_2
made_off_dribble_3
made_post_2




if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    player_data = pd.read_csv('~/capstone_project/data/aggregated_player_data.csv')
