import numpy as np
import pandas as pd
import os
from sklearn.manifold import TSNE
from utils import save_params, check_repeated_params, unpack_params

# Does tsne mapping from middle dimensionality to small dimensionality
# Loads data set from mid_dataset_path and saves reduced dataset in save_to_path
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def tsne_small (save_to_path, mid_dataset_path, **kwargs):

    d = kwargs
    mid_X = pd.read_csv(mid_dataset_path, header=None)
    unique_ids = mid_X.values[:,0].reshape(mid_X.shape[0],1)
    mid_X = mid_X.values[:,1:]
    
    tsne_model = TSNE(n_components=d['components'], perplexity=d['perplexity'],
                      learning_rate=d['learning_rate'], n_iter=d['iterations'], random_state=d['random_state'])
    small_X = tsne_model.fit_transform(mid_X)

    # small_X = mid_X[:,[0,1]]
    small_X = pd.DataFrame(np.hstack((unique_ids,small_X)))
    small_X.to_csv(save_to_path, index=False, header=False)

# Does pca mapping from middle dimensionality to small dimensionality
def pca_small (filename):
    pass

# Perform dimensionality reduction from middle dimensionality to small dimensionality
# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params list is the combination of parameters to be used for this step
def reduce_to_small_dimension (params_path, params_list):

    save_to = 'small_dataset'
    for i in params_list:
        save_to += '_' + str(i)
    save_to += '.csv'
    save_to = os.path.join(params_path[-1], save_to)

    load_from = 'mid_dataset'
    for i in params_list[:-1]:
    	load_from += '_' + str(i)
    load_from += '.csv'
    load_from = os.path.join(params_path[-2], load_from)

    curr_params = unpack_params(params_path, params_list)

    print("Performing small dimensionality reduction...")
    print("Using parameters: " + str(curr_params))
    print("Saving at: " + save_to)
    print("Loading from: " + load_from)

    if os.path.exists(save_to):
        print ("Small dimensionality reduction for these parameters already done!")
        return

    # Perform dimensionality reduction using the preferred parameters
    if curr_params['small_algorithm'] == "tsne":
        tsne_small(save_to, load_from, **curr_params)
    elif curr_params['small_algorithm'] == "pca":
        pca_small(save_to, load_from, **curr_params)
    

if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    mid_dim_path = 'mid_datasets'
    small_dim_path = 'small_datasets'
    params_path = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path]

    # Define possible parameters for small dimensionality reduction
    param_set_1 = {'small_algorithm': 'tsne', 'components': 2, 'perplexity': 30, 'learning_rate': 200, 'iterations': 5000}
    param_set_2 = {'small_algorithm': 'tsne', 'components': 3, 'perplexity': 30, 'learning_rate': 200, 'iterations': 5000}
    save_params(small_dim_path, **param_set_1)
    save_params(small_dim_path, **param_set_2)
    
    # Define the sets of parameters to use
    preproc_params = 2
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 2
    params_list = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params]

    # reduce_to_small_dimension(params_path, params_list)


