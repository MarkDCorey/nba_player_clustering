import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram


#
kmeans = KMeans()
kmeans.fit()

#Need process to index/scale the data
def data_scaling(df):
    pass

#look for interpretability in the clusters.
#ideally there is significant separation (eg standard dev from average of player set) on a subset of features
#either use these features to define the cluster labels, or come up with own

print "cluster centers:"
print kmeans.cluster_centers_

top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
print "top features for each cluster:"
for num, centroid in enumerate(top_centroids):
    print "%d: %s" % (num, ", ".join(features[i] for i in centroid))



if __name__ == '__main__':
    #read in the aggregated/saved data into a df
    player_data = pd.read_csv('file')
