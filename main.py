import sys
from utils import save_params, check_repeated_params, unpack_params, get_id, init_unique_id_dict, user_confirmation
from clip_extraction import get_file_formats, make_directory_copy, make_cover_art_copy, extract_all_clips, copy_clips_to_single_folder
from create_ids import assign_unique_ids
from feature_extraction import perform_feature_extraction
from mid_dimension import reduce_to_mid_dimension
from small_dimension import reduce_to_small_dimension
from clustering import perform_clustering
from visualization import perform_visualization


# Formats to consider for making a local copy (music and cover art)
aud_formats = set(['.wav', '.m4a', '.WAV', '.aiff', '.aif'])
img_formats = set(['.tif', '.jpg', '.JPG', '.png'])

# Need to be absolute paths (start with '/')
# Assumes Mac connected to the CDS-Carlos server (might need to modify server_path for Windows)
# NOT WORKING ON WINDOWS AT THE MOMENT - Path names are too long and Windows has a character limit!
server_path = "/Volumes/CDS-Carlos"
local_path = "/Users/masc/Documents/Oscar/MaSC-Music-Visualization-master/Server_Copy"

# Local folders for preprocessing parameters
preproc_path = 'preprocessing'
feature_ext_path = 'full_datasets'
mid_dim_path = 'mid_datasets'
small_dim_path = 'small_datasets'


if __name__ == "__main__":
    
    # ----- Initialization ----- #

    # user_confirmation()
    # get_file_formats(server_path)

    # user_confirmation()
    # make_directory_copy(server_path, local_path)

    # user_confirmation()
    # make_cover_art_copy(server_path, local_path, img_formats)

    # user_confirmation()
    # extract_all_clips(server_path, local_path, aud_formats, location='middle', length=15)

    # user_confirmation()
    # copy_clips_to_single_folder(local_path, ['.wav'], location='middle', length=15)

    # user_confirmation()
    # assign_unique_ids(server_path, aud_formats, 'CDS-Carlos_song_ids_test.csv')

    user_confirmation()
    # Initialize dictionary for Unique-IDs and names
    ids_dict = init_unique_id_dict ('CDS-Carlos_song_ids.csv')

    
    # ----- Preprocessing ----- #
    user_confirmation()

    # Define possible parameters for preprocessing
    param_set_1 = {'sr': 22050, 'window_size': 23, 'hop_length': 512, 'server_subpaths': 'All'}
    param_set_2 = {'sr': 44100, 'window_size': 50, 'hop_length': 2205, 'server_subpaths': 'All'}
    param_set_3 = {'sr': 44100, 'window_size': 50, 'hop_length': 2205, 'server_subpaths': 'FINAL_East African Popular Music Archive'}
    # Set the hop length; at 22050 Hz, 512 samples ~= 23ms  # at 44100Hz, for 50ms use 2205 as hop_length

    save_params(preproc_path, **param_set_1)
    save_params(preproc_path, **param_set_2)
    save_params(preproc_path, **param_set_3)



    # ----- Feature extraction ----- #
    user_confirmation()

    # Define possible parameters for feature extraction
    for method in ['mfcc', 'spectrogram']:
        for duration in [5, 10]:
            save_params(feature_ext_path, method=method, duration=duration)
    
    # Define a set of preprocessing parameters and a set of feature extraction parameters to use
    preproc_params = 3
    feature_ext_params = 1
    params_list = [preproc_params, feature_ext_params]

    # Define the audio clips to be used
    audio_path = 'middle_15'

    # List containing the parameter folder paths
    params_path = [preproc_path, feature_ext_path]

    perform_feature_extraction(ids_dict, params_path, params_list, audio_path)



    # ----- Middle dimensionality ----- #
    user_confirmation()

    # Define possible parameters for middle dimensionality reduction
    param_set_1 = {'mid_algorithm': 'identity'}

    save_params(mid_dim_path, **param_set_1)
    
    # Define the sets of parameters to use
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    params_list = [preproc_params, feature_ext_params, mid_dim_params]

    # List containing the parameter folder paths
    params_path = [preproc_path, feature_ext_path, mid_dim_path]

    reduce_to_mid_dimension(params_path, params_list)

    

    # ----- Small dimensionality ----- #
    user_confirmation()

    # Define possible parameters for small dimensionality reduction
    param_set_1 = {'small_algorithm': 'tsne', 'components': 2, 'perplexity': 30, 'learning_rate': 200, 'iterations': 5000, 'random_state': 0}
    param_set_2 = {'small_algorithm': 'tsne', 'components': 3, 'perplexity': 30, 'learning_rate': 200, 'iterations': 5000, 'random_state': 0}
    save_params(small_dim_path, **param_set_1)
    save_params(small_dim_path, **param_set_2)
    
    # Define the sets of parameters to use
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 1
    params_list = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params]

    # List containing the parameter folder paths
    params_path = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path]

    reduce_to_small_dimension(params_path, params_list)



    # ----- Small dimensionality ----- #
    user_confirmation()

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    mid_dim_path = 'mid_datasets'
    small_dim_path = 'small_datasets'
    clustering_path = 'clustering_labels'
    params_path = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path, clustering_path]

    # Define possible parameters for clustering
    param_set_1 = {'clustering_algorithm': 'kmeans', 'n_clusters': 5}
    save_params(clustering_path, **param_set_1)
    
    # Define the sets of parameters to use
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 1
    clustering_params = 1
    params_list = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params, clustering_params]

    perform_clustering(params_path, params_list)



    # ----- Small dimensionality ----- #
    user_confirmation()

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    mid_dim_path = 'mid_datasets'
    small_dim_path = 'small_datasets'
    clustering_path = 'clustering_labels'
    params_path_data = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path]
    params_path_clusters = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path, clustering_path]
    
    # Define the sets of parameters to use for dataset (has to be from small_datasets)
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 1
    params_list_data = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params]

    # Define the sets of parameters to use for clustering labels (can be any of full, mid or small datasets on the same branch)
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 1
    clustering_params = 1
    params_list_clusters = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params, clustering_params]

    # Define the audio clips to be used
    audio_path = 'middle_15'

    perform_visualization(params_path_data, params_path_clusters, params_list_data, params_list_clusters, audio_path)
