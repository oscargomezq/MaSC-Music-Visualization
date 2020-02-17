import os
import numpy as np
import pandas as pd
import jellyfish
from sklearn.neighbors import NearestNeighbors
from utils import save_params, check_repeated_params, unpack_params, user_confirmation, init_unique_id_dict, get_key


# Assign each song in the server an artist to use for the analysis
# Prompts the user to assign an artist selected from one of the subfolders in the path
def assign_artist (group_arr):

    all_subfolders = os.path.normpath(group_arr[0][1]).split(os.path.sep)

    while True:
	    print()
	    print ("Enter number for the artist:")
	    for i in range(len(all_subfolders)):
	        print (i, "---", all_subfolders[i])
	    print("M", "---", "Enter artist manually")
	    print()
	    artist_idx = input("Number or 'M': ")

	    poss_inp = ['M']
	    poss_inp.extend( [str(x) for x in range(len(all_subfolders))] )
	    if artist_idx in poss_inp:
	    	break
	    else:
	    	print ("Invalid input")

    if artist_idx == "M":
        artist = input("Please enter artist name for this group: ")
    else:
    	artist = all_subfolders[int(artist_idx)]

    print(artist)
    group_arr = group_arr.tolist()
    group_arr = [x + [artist] for x in group_arr]
    group_arr = np.array(group_arr)
    return group_arr

# Go through all the IDs and assign metadata to each leaf subfolder (By album or more granular)
def perform_metadata_input (ids_csv_path, save_to):

    # Open IDs file
    ids_df = pd.read_csv(ids_csv_path, header=None, encoding='utf-8')
    ids_arr = ids_df.values
    group_cnt = 0

    leaf_dir = os.path.normpath(ids_arr[0][1]).split(os.path.sep)[-2]

    if os.path.exists(save_to):
    	stats_df = pd.read_csv(save_to, header=None, encoding='utf-8')
    	start = stats_df.values.shape[0]
    else:
    	start = 1
    idx = start-1
    for i in range(start,ids_arr.shape[0]):
        all_subfolders = os.path.normpath(ids_arr[i][1]).split(os.path.sep)
        curr_leaf = all_subfolders[-2] 

        # Identify group in the same leaf subfolder
        if (curr_leaf != leaf_dir) or (i==ids_arr.shape[0]-1):

            # Make nparray of the group
            if i==ids_arr.shape[0]-1:
                group = ids_arr[idx:i+1,:]
            else:
                group = ids_arr[idx:i,:]

            # Prompt user to assign artist based on the list of subfolders or a manual entry
            # Call assign artist
            group_update = assign_artist(group)

            # Calls to other methods
            # Updated dataframe returned in group_update

            # Append to the corpus_statistics file
            with open(save_to, 'a', encoding='utf-8') as stats_file:
            	print(group_update)
            	for entry in group_update:
            		print(entry)
            		for col_idx in range(len(entry)-1):
            			stats_file.write('\"' + str(entry[col_idx]) + '\",')
            		stats_file.write('\"' + str(entry[len(entry)-1]) + '\"')
            		stats_file.write('\n')

            print(leaf_dir)
            print("Songs in this group:", group_update.shape[0])
            print("------------------------------")

            idx = i
            leaf_dir = curr_leaf
            group_cnt += 1

    print()
    print("Total leaf groups:", group_cnt)

# Detect possible duplicate files in the collection using nearest neighbors from a reduced dimensionality dataset
# Saves csv file with possible duplicate list for each song, return path to this csv file
def detect_poss_duplicates (ids_dict, params_path_data, params_list_data, n_neighbors = 5):
	
	curr_params_data = unpack_params(params_path_data, params_list_data)

	load_from_data = 'small_dataset'
	for i in params_list_data:
		load_from_data += '_' + str(i)
	load_from_data += '.csv'
	load_from_data = os.path.join(params_path_data[-1], load_from_data)

	save_to = 'possible_duplicates'
	save_to += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		save_to += '_' + str(i)
	save_to += ').csv'

	print("Creating possible duplicates file...")
	print("Using dataset parameters: " + str(curr_params_data))
	print("Saving at: " + save_to)
	print("Loading dataset from: " + load_from_data)

	df_dups = pd.read_csv(load_from_data, names=['UniqueID', 'f1', 'f2'])
	matrix_2d = df_dups.values[:,1:]
	
	neigh = NearestNeighbors(n_neighbors=n_neighbors)
	neigh.fit(matrix_2d)
	dist_mat, idx_mat = neigh.kneighbors(matrix_2d)

	df_dups['name'] = [ os.path.split(get_key(df_dups.iloc[j,0], ids_dict))[1] for j in range(idx_mat.shape[0])]

	for i in range(n_neighbors):
		df_dups['uid_'+str(i)] = [ df_dups.iloc[x,0] for x in idx_mat[:,i] ]
		df_dups['name_'+str(i)] = [ os.path.split(get_key(df_dups.iloc[idx_mat[j,i],0], ids_dict))[1] for j in range(idx_mat.shape[0]) ]
		df_dups['sound_dist_'+str(i)] = dist_mat[:,i]
		df_dups['name_dist_'+str(i)] = [ jellyfish.jaro_winkler (df_dups['name'][j], df_dups['name_'+str(i)][j]) for j in range(idx_mat.shape[0]) ]	
	
	df_dups.to_csv(save_to, index=False, header=True)

	return save_to

# For each possible duplicate under a given distance:
# 1. check the original filepath and mark as duplicate is one is suffix of the other / manually
# 2. play excerpts to confirm if duplicates
def mark_duplicates(ids_dict, params_path_data, params_list_data, n_neighbors = 5):

	poss_dups_path = 'possible_duplicates'
	poss_dups_path += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		poss_dups_path += '_' + str(i)
	poss_dups_path += ').csv'

	save_to = poss_dups_path.replace("possible", "confirmed")

	print("Creating confirmed duplicates file...")
	print("Saving at: " + save_to)
	print("Loading dataset from: " + poss_dups_path)

	df_dups = pd.read_csv(poss_dups_path)
	to_drop = ['dist_'+str(x) for x in range(n_neighbors)]
	to_drop.append('f1')
	to_drop.append('f2')
	to_drop.append('uid_0')
	df_dups = df_dups.drop(to_drop, axis=1)

	dups_dict = dict(zip(df_dups.values[:,0], df_dups.values[:,1:].tolist()))
	for uid in dups_dict:
		print(uid)
		print(get_key(uid, ids_dict))
		for j in dups_dict[uid]:
			print(get_key(j, ids_dict))
		print()
		# print(dups_dict[uid])

	return

	df_dups.to_csv(save_to, index=False, header=True)


if __name__ == "__main__":

	# Path to save the file that contains all metadata
	metadata_path = "corpus_statistics.csv"

	# Manually input metadata for the collection (artists, years, etc.)
	# perform_metadata_input('CDS-Carlos_song_ids.csv', metadata_path)

	   
	# Duplicate removal

	# Initialize dictionary for Unique-IDs and names
	ids_dict = init_unique_id_dict ('CDS-Carlos_song_ids.csv')

	# Local folders for preprocessing parameters
	preproc_path = 'preprocessing'
	feature_ext_path = 'full_datasets'
	mid_dim_path = 'mid_datasets'
	small_dim_path = 'small_datasets'
	clustering_path = 'clustering_labels'
	params_path_data = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path]

	# Define the sets of parameters to use for dataset (has to be from small_datasets)
	preproc_params = 3
	feature_ext_params = 1
	mid_dim_params = 1
	small_dim_params = 3
	params_list_data = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params]

	# Compute possible duplicate songs in the collection
	poss_dups_path = detect_poss_duplicates (ids_dict, params_path_data, params_list_data)

	# Mark confirmed duplicate songs
	# mark_duplicates(ids_dict, params_path_data, params_list_data)
