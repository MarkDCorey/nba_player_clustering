from scipy import stats
import pandas as pd


scored = cluster_groups['points_scored'].sum()
allowed = cluster_groups['points_allowed'].sum()
#sanity check: plus_minus (scored - allowed) should be ~ 0

#eliminate groups where points or minutes volume is too small
#how to determine where this threshold is?

#after the prior step, do the above sanity check again
#may need to calculate new mean plus_minus

#take the variance on the plus_minus across remaining groups
plus_minus_var = cluster_groups['plus_minus'].var()

#get the SEM
stats.sem(cluster_groups['plus_minus'])


if __name__ == '__main__':
    #run cluster overlay script to produce DF
    # cluster_groups = ....
