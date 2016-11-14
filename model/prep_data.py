#feature creation and scaling the data for the model

player_id
age
display_name
dleague_flag
first_name
last_name
position
roster_status
season_exp
team_id
team_name
# attempt_2
# attempt_3
# attempt_at_rim_2
# attempt_cut_run_2
# attempt_drive_2
# attempt_jumper_2
# attempt_jumper_3
# attempt_off_dribble_2
# attempt_off_dribble_3
# attempt_post_2
made_2
made_3
# made_at_rim_2
# made_cut_run_2
# made_drive_2
# made_jumper_2
# made_jumper_3
# made_off_dribble_2
# made_off_dribble_3
# made_post_2
total_attempt
total_made
# catch_shoot_freq
ast
blk
blk_a
dreb
fta
ftm
gp
min_game
oreb
pf
pfd
reb
stl
tov
c_dreb_game
c_oreb_game
avg_speed_def
avg_speed_off
avg_speed_tot
mi_game_def
mi_game_off
mi_game_tot
d_fga_overall
d_fga_paint
d_fga_perim
d_fgm_overall
d_fgm_paint
d_fgm_perim
d_ppm_overall
d_ppm_paint
d_ppm_perim
pass_total



#include
labels = [player_id]
features = [age,season_exp,catch_shoot_freq]


#new vars
min_tot = gp * min_game

ast_per_min = ast/min_tot
blk_per_min = blk/min_tot
blk_a_per_min = blk_a/min_tot
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


attempt_at_rim_2_per_min = attempt_at_rim_2/min_tot
attempt_cut_run_2_per_min = attempt_cut_run_2/min_tot
attempt_drive_2_per_min = attempt_drive_2/min_tot
attempt_jumper_2_per_min = attempt_jumper_2/min_tot
attempt_jumper_3_per_min = attempt_jumper_3/min_tot
attempt_off_dribble_2_per_min = attempt_off_dribble_2/min_tot
attempt_off_dribble_3_per_min = attempt_off_dribble_3/min_tot
attempt_post_2_per_min = attempt_post_2/min_tot

made_at_rim_2_per_min = made_at_rim_2/min_tot
made_cut_run_2_per_min = made_cut_run_2/min_tot
made_drive_2_per_min = made_drive_2/min_tot
made_jumper_2_per_min = made_jumper_2/min_tot
made_jumper_3_per_min = made_jumper_3/min_tot
made_off_dribble_2_per_min = made_off_dribble_2/min_tot
made_off_dribble_3_per_min = made_off_dribble_3/min_tot
made_post_2_per_min = made_post_2/min_tot




if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    player_data = pd.read_csv('~/capstone_project/data/aggregated_player_data.csv')
