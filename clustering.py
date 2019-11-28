import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils import save_params, check_repeated_params, unpack_params, user_confirmation

# Plot the inertia for different values of k for kmeans to select an optimal k
def select_kmeans(dataset_path, **kwargs):

    d = kwargs
    X = pd.read_csv(dataset_path, header=None)
    unique_ids = X.values[:,0].reshape(X.shape[0],1)
    X = X.values[:,1:]
    # scaler = StandardScaler()
    # X = scaler.fit_transform(X)

    x_plot = range(1,20)
    y_plot = []
    for k in x_plot:
    	kmeans = KMeans(n_clusters=k, random_state=d['random_state']).fit(X)
    	inertia_X = kmeans.inertia_
    	y_plot.append(inertia_X)
    	print (k, inertia_X)
    plt.plot(x_plot, y_plot)
    plt.show()

# Does kmeans clustering on the dataset given
# Loads data set from dataset_path and saves the labels in save_to_path
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def cluster_kmeans(save_to_path, dataset_path, **kwargs):

	d = kwargs
	X = pd.read_csv(dataset_path, header=None)
	unique_ids = X.values[:,0].reshape(X.shape[0],1)
	X = X.values[:,1:]
	# scaler = StandardScaler()
	# X = scaler.fit_transform(X)

	kmeans_model = KMeans(n_clusters=d['n_clusters'], random_state=d['random_state']).fit(X)
	labels_X = kmeans_model.labels_.reshape(X.shape[0],1)
	inertia_X = kmeans_model.inertia_

	labels_X = pd.DataFrame(np.hstack((unique_ids,labels_X)))
	labels_X.to_csv(save_to_path, index=False, header=False)

# Perform clustering on the dataset
# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params list is the combination of parameters to be used for this step
def perform_clustering(params_path, params_list):

	params_len = len(params_list)-1

	save_to = 'cluster_labels'
	save_to += '_(' + str(params_list[0])
	for i in params_list[1:-1]:
		save_to += '_' + str(i)
	save_to += ')_' + str(params_list[-1])
	save_to += '.csv'
	save_to = os.path.join(params_path[-1], save_to)

	load_from = 'full_dataset' if params_len == 2 else ('mid_dataset' if params_len == 3 else 'small_dataset' )
	for i in params_list[:-1]:
		load_from += '_' + str(i)
	load_from += '.csv'
	load_from = os.path.join(params_path[-2], load_from)

	curr_params = unpack_params(params_path, params_list)

	print("Performing clustering...")
	print("Using parameters: " + str(curr_params))
	print("Saving at: " + save_to)
	print("Loading from: " + load_from)

	if os.path.exists(save_to):
		print ("Clustering for these parameters already done!")
		return

	# Perform clustering using the preferred parameters
	if curr_params['clustering_algorithm'] == "kmeans":
		inp = user_confirmation("Enter 'select' to plot kmeans inertia for various k, \n'c' to continue," )
		if inp == 'select':
			select_kmeans(load_from, **curr_params)
		cluster_kmeans(save_to, load_from, **curr_params)


if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    # mid_dim_path = 'mid_datasets'
    # small_dim_path = 'small_datasets'
    clustering_path = 'clustering_labels'
    params_path = [preproc_path, feature_ext_path, clustering_path]

    # Define possible parameters for clustering
    param_set_1 = {'clustering_algorithm': 'kmeans', 'n_clusters': 5}
    save_params(clustering_path, **param_set_1)
    
    # Define the sets of parameters to use
    preproc_params = 3
    feature_ext_params = 1
    # mid_dim_params = 1
    # small_dim_params = 1
    clustering_params = 1
    params_list = [preproc_params, feature_ext_params, clustering_params]

    perform_clustering(params_path, params_list)