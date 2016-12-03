NBA PLAYER TYPES AND OPTIMAL LINEUP COMPOSITION


PROJECT DESCRIPTION

-I used unsupervised machine learning to cluster NBA players by style of play.  The resulting clusters were then merged with lineup performance data in order to derive insights about successful lineup composition


APPLICATIONS

-Finding latent improvement opportunities (eg lineup composition, players to pursue through trade, draft or free-agency) for any team.

-Projecting rookie and college player cluster and NBA player comps.

-Determining unique player valuation for each team.

-Discovering whether new lineup composition trends are developing.


PROCESS OUTLINE

-Scraped player and lineup statistics from NBA.com/Stats.

-Created feature set of 15 per-possession offensive and defensive actions of players to capture player style.

-Built clustering model using multi-step approach:

    -Applied agglomerative hierarchical clustering to identify three large spherical parent clusters with significant inter-cluster separation

    -Significantly reduced dimensionality of each parent cluster using principle component analysis

    -Applied t-Distributed Stochastic Neighbor Embedding to each parent cluster.  t-SNE is used here to identify instances of non-spherical clustering within each parent, and to remap the points to a new space where the notion of distance between points is derived from regional density variations

    -K-means is then applied to each of the three remapped groups of points, where its inherent spherical cluster assumption is now able to successfully capture non-spherical patterns

    -Iterated through possible k-values for each parent to identify optimal k-value based on levels of intra-cluster inertia and inter-cluster separation

-Described each cluster by determining its lift for each feature in standard deviations from the the mean for that feature across the full dataset.  

-Merged the resulting cluster labels for each player with the lineup level data. Used net-scoring-margin-per-minute as metric to compare lineup performance.

-Grouped lineup data by cluster combination and ran z-test for each cluster combination to determine the statistical significance of lift relative to the population of lineups.
