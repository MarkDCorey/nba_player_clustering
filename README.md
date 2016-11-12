# nba_player_clustering

PROJECT DESCRIPTION

o	Determine whether we can meaningfully cluster players NBA players by "type"
o	Use this info to determine whether there are optimal compositions of player types when forming teams and lineups?  If there are optimal compositions, we can potentially....
o	identify latent improvement opportunities for any team (eg new lineups to test, prioritization of players to pursue via free-agency or trade).
o	predict any player's value to any team.
o	determine whether optimal team/lineup compositions have changed over time.
o	determine whether new trends in team/lineup compositions are developing.


PROCESS OUTLINE

o	Identify player feature set and k value, and build player clusters.
o	Merge the resulting cluster labels with NBA's lineup data
o	Translate each lineup into appropriate cluster labels
o	Aggregate identical cluster combos
o	Index and sort the cluster combos by a weighted average of NetRating*
o	Determine statistical significance of the "best" cluster combos
o	Analysis
o	Understand the characteristic features of each cluster
o	Score players within clusters and use these rankings, along with the cluster rankings, to identify areas of opportunity for the teams
o	Look for patterns of changing composition over time and whether new patterns are emerging.
