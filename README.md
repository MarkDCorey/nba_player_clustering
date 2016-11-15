# nba_player_clustering

PROJECT DESCRIPTION

Determine whether we can meaningfully cluster players NBA players by "type"


Use this info to determine whether there are optimal compositions of player types when forming teams and lineups.  If there are optimal compositions, we can potentially....

  -identify latent improvement opportunities for any team (eg new lineups to test,     prioritization of players to pursue via free-agency or trade).

  -predict any player's value to any team.

  -determine whether optimal team/lineup compositions have changed over time.

  -determine whether new trends in team/lineup compositions are developing.


PROCESS OUTLINE

-Identify player feature set and k value, and build player clusters.

-Merge the resulting cluster labels with NBA's lineup data and translate each lineup into appropriate cluster labels

-Aggregate identical cluster combos

-Index and sort the cluster combos by a weighted average of NetRating, then determine statistical significance of the "best" cluster combos


ANALYSIS

-Understand the characteristic features of each cluster

-Score players within clusters and use these rankings, along with the cluster rankings, to identify areas of opportunity for the teams

-Look for patterns of changing composition over time and whether new patterns are emerging.
