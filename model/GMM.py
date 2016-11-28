from sklearn import mixture, decomposition, preprocessing
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



featurized_data = pd.read_csv('~/capstone_project/data/featurized_data.csv')
player_mat = featurized_data[featurized_data.min_tot >200]
player_info = player_mat[['player_id','display_name']]
player_mat.drop(['player_id','display_name','min_tot','gp'], inplace = True, axis = 1)
player_mat.fillna(0, inplace = True)
player_mat = preprocessing.scale(player_mat)

 #
 # gmm = mixture.GMM(n_components=1, covariance_type='diag',
 #    random_state=None, thresh=None, tol=0.001, min_covar=0.001, n_iter=100, n_init=1,
 #    params='wmc', init_params='wmc', verbose=0)

clf = mixture.GMM(11, n_iter = 500, random_state = 3).fit(player_mat)

clusters = clf.predict(player_mat)
player_info['cluster'] = clusters
player_info.to_csv('~/capstone_project/data/gmm_clusters.csv')


#mean value per gaussian for each feature
#clf.means_

#coveariance per gausian for each feature
#clf.covars_

#weights
#clf.weights_

'''
These individual Gaussian distributions are fit using
an expectation-maximization method, much as in K means,
except that rather than explicit cluster assignment,
the posterior probability is used to compute the weighted
mean and covariance. Somewhat surprisingly, this
algorithm provably converges to the optimum (though the
optimum is not necessarily global).
'''

n_estimators = np.arange(1, 18)
clfs = [mixture.GMM(n, n_iter=1000).fit(player_mat) for n in n_estimators]
bics = [clf.bic(player_mat) for clf in clfs]
aics = [clf.aic(player_mat) for clf in clfs]

plt.plot(n_estimators, bics, label='BIC')
plt.plot(n_estimators, aics, label='AIC')
plt.legend()
plt.savefig("bic_aic.png", dpi= 300)
plt.show();
