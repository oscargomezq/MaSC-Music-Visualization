import numpy as np
import pandas as pd
import os
import plotly.express as px
import plotly
from utils import save_params, check_repeated_params, unpack_params, user_confirmation

# Create 2d visualization on the dataset and clusters given
# Loads data set from dataset_path and the labels from clustering_path
# Saves visualization to save_to_path as HTML
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def bokeh_2d(save_to_path, dataset_path, clustering_path, **kwargs):
	pass

# Create 3d visualization on the dataset and clusters given
# Loads data set from dataset_path and the labels from clustering_path
# Saves visualization to save_to_path as HTML
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def pyplot_3d(save_to, load_from_data, load_from_clusters, **curr_params_data):
	df = pd.read_csv(load_from_data)
	print(df.head())
	# fig = px.scatter_3d(df, x='f1', y='f2', z='f3', color='color')
	# plotly.io.write_html(fig, file=save_to, auto_open=False)
	

# Perform 2d or 3d visualization on the dataset given with the clustering labels given
# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params_list_data is the combination of parameters for the dataset to use
# params_list_clusters is the combination of parameters for the cluster labels to use
def perform_visualization(params_path_data, params_path_clusters, params_list_data, params_list_clusters):

	curr_params_data = unpack_params(params_path_data, params_list_data)
	curr_params_clusters = unpack_params(params_path_clusters, params_list_clusters)

	dim = curr_params_data['components']

	save_to = '2D_visualization_labels' if dim == 2 else ('3D_visualization_labels' if dim == 3 else 'invalid')
	save_to += '_(' + str(params_list_clusters[0])
	for i in params_list_clusters[1:-1]:
		save_to += '_' + str(i)
	save_to += ')_'
	save_to += str(params_list_clusters[-1])
	save_to += '_data'
	save_to += '_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		save_to += '_' + str(i)
	save_to += ')'
	save_to += '.html'
	save_to = os.path.join('visualizations', save_to)

	load_from_data = 'small_dataset'
	for i in params_list_data:
		load_from_data += '_' + str(i)
	load_from_data += '.csv'
	load_from_data = os.path.join(params_path_data[-1], load_from_data)

	load_from_clusters = 'cluster_labels'
	load_from_clusters += '_(' + str(params_list_clusters[0])
	for i in params_list_clusters[1:-1]:
		load_from_clusters += '_' + str(i)
	load_from_clusters += ')_'
	load_from_clusters += str(params_list_clusters[-1])
	load_from_clusters += '.csv'	
	load_from_clusters = os.path.join(params_path_clusters[-1], load_from_clusters)


	print("Creating visualization...")
	print("Using dataset parameters: " + str(curr_params_data))
	print("Using clustering parameters: " + str(curr_params_clusters))
	print("Saving at: " + save_to)
	print("Loading dataset from: " + load_from_data)
	print("Loading clusters from: " + load_from_clusters)

	if os.path.exists(save_to):
		print ("Clustering for these parameters already done!")
		return

	# Create visualization using the preferred parameters
	if dim == 2:
		bokeh_2d(save_to, load_from_data, load_from_clusters, **curr_params_data)
	elif dim == 3:
		pyplot_3d(save_to, load_from_data, load_from_clusters, **curr_params_data)


if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    mid_dim_path = 'mid_datasets'
    small_dim_path = 'small_datasets'
    clustering_path = 'clustering_labels'
    params_path_data = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path]
    params_path_clusters = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path, clustering_path]

    # # Define possible parameters for clustering
    # param_set_1 = {'clustering_algorithm': 'kmeans', 'n_clusters': 5}
    # save_params(clustering_path, **param_set_1)
    
    # Define the sets of parameters to use for dataset (has to be from small_datasets)
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 2
    params_list_data = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params]

    # Define the sets of parameters to use for clustering labels (can be any of full, mid or small datasets on the same branch)
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 2
    clustering_params = 1
    params_list_clusters = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params, clustering_params]

    perform_visualization(params_path_data, params_path_clusters, params_list_data, params_list_clusters)


    