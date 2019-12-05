import numpy as np
import pandas as pd
import os
import shutil
from utils import save_params, check_repeated_params, unpack_params

# Does identity mapping from full dimensionality to middle dimensionality
# Loads data set from full_dataset_path and saves reduced dataset in save_to_path
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def identity_mid (save_to_path, full_dataset_path, **kwargs):
    shutil.copy(full_dataset_path, save_to_path)

def pca_mid (filename):
    pass

def autoencoder_mid (filename):
    pass


# Perform dimensionality reduction from full dimensionality to middle dimensionality
# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params list is the combination of parameters to be used for this step
def reduce_to_mid_dimension (params_path, params_list):

    save_to = 'mid_dataset'
    for i in params_list:
        save_to += '_' + str(i)
    save_to += '.csv'
    save_to = os.path.join(params_path[-1], save_to)

    load_from = 'full_dataset'
    for i in params_list[:-1]:
        load_from += '_' + str(i)
    load_from += '.csv'
    load_from = os.path.join(params_path[-2], load_from)

    curr_params = unpack_params(params_path, params_list)

    print("Performing middle dimensionality reduction...")
    print("Using parameters: " + str(curr_params))
    print("Saving at: " + save_to)
    print("Loading from: " + load_from)

    if os.path.exists(save_to):
        print ("Middle dimensionality reduction for these parameters already done!")
        return

    # Perform dimensionality reduction using the preferred parameters
    if curr_params['mid_algorithm'] == "identity":
        identity_mid(save_to, load_from, **curr_params)
    elif curr_params['mid_algorithm'] == "pca":
        pca_mid(save_to, load_from, **curr_params)
    

if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    mid_dim_path = 'mid_datasets'
    params_path = [preproc_path, feature_ext_path, mid_dim_path]

    # Define possible parameters for middle dimensionality reduction
    param_set_1 = {'mid_algorithm': 'identity', 'standardize_mid': 'True'}
    param_set_2 = {'mid_algorithm': 'pca', 'standardize_mid': 'True'}
    param_set_3 = {'mid_algorithm': 'autoencoder', 'standardize_mid': 'True'}

    save_params(mid_dim_path, **param_set_1)
    save_params(mid_dim_path, **param_set_2)
    save_params(mid_dim_path, **param_set_3)
    
    # Define the sets of parameters to use
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    params_list = [preproc_params, feature_ext_params, mid_dim_params]

    reduce_to_mid_dimension(params_path, params_list)


