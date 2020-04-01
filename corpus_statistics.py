import os
import numpy as np
import pandas as pd
import jellyfish
import pygame
import time
from sklearn.neighbors import NearestNeighbors
from utils import save_params, check_repeated_params, unpack_params, user_confirmation, init_unique_id_dict, get_key

# True if a is a prefix or suffix of b or viceversa
def is_psfix (a, b):
	return int(a.startswith(b) or b.startswith(a) or a.endswith(b) or b.endswith(a))

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
# For each nearest neighbor, record the "sound" distance, "name" distance, and whether it is a suffix or prefix of the other.
# Saves csv file with possible duplicate list for each song
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
		df_dups['name_dist_'+str(i)] = [ -jellyfish.jaro_winkler (df_dups['name'][j], df_dups['name_'+str(i)][j]) + 1 for j in range(idx_mat.shape[0]) ]	
		df_dups['is_psfix_'+str(i)] = [ is_psfix (df_dups['name'][j], df_dups['name_'+str(i)][j]) for j in range(idx_mat.shape[0]) ]

	to_drop = ['f1','f2']
	df_dups = df_dups.drop(to_drop, axis=1)
	df_dups.to_csv(save_to, index=False, header=True, encoding='utf-8')

# Helper function
def create_categories ():
	categories = []
	for st in ["above_st", "below_st"]:
		for nt in ["above_nt", "below_nt"]:
			for pt in ["psfix", "not_psfix"]:
				categories.append(st + "--" + nt + "--" + pt)
	return categories

# Helper function returning the category as a string
def assign_category (s, n, ps, st, nt, pst):
	category = ""
	category += ("above_st" if s>st else "below_st")
	category += "--"
	category += ("above_nt" if n>nt else "below_nt")
	category += "--"
	category += ("psfix" if ps==pst else "not_psfix")
	return category

# For each category decide if it is surely duplicate, surely not, or needs further revision
def assign_category_outcome (uuid1, uuid2, category):

	# 1 = surely duplicate
	# -1 = surely not duplicate
	# 0 = needs further revision

	if category == "below_st--below_nt--psfix":
		return (-1 if uuid1 == uuid2 else 1) # -1 when it's comparing with itself, 1 if not

	else:
		poss_cats = [ "below_st--below_nt--not_psfix",
					  "below_st--above_nt--psfix",
					  "below_st--above_nt--not_psfix",
					  "above_st--below_nt--psfix",
					  "above_st--above_nt--psfix" ]

		imposs_cats = [ "above_st--below_nt--not_psfix",
					    "above_st--above_nt--not_psfix" ]

		return 0 if (category in poss_cats) else -1

# For each possible duplicate mark the category it belongs to according to the thresholds it passes in:
# 1. Sound distance: Euclidean distance in the 2D projection
# 2. Name distance: Jaro-Winkler distance between the filenames
# 3. Suffix of prefix: If one filename is a p(s)-fix of the other
def mark_duplicate_categories (ids_dict, params_path_data, params_list_data, n_neighbors = 5):

	poss_dups_path = 'possible_duplicates'
	poss_dups_path += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		poss_dups_path += '_' + str(i)
	poss_dups_path += ').csv'

	save_to = poss_dups_path.replace("possible", "categories")

	print("Creating categories duplicates file...")
	print("Saving at: " + save_to)
	print("Loading dataset from: " + poss_dups_path)

	categories = create_categories()
	df_dups = pd.read_csv(poss_dups_path, encoding="utf-8")

	# Decide confidence thresholds
	SOUND_D_THR = 0.3    # Could test between 0.3 - 0.6
	NAME_D_THR = 0.6     # Could test between 0.6 - 0.12 
	IS_PSFIX_THR = True

	for i in range(n_neighbors):
		df_dups['cat_'+str(i)] = [ assign_category( df_dups['sound_dist_'+str(i)][j], df_dups['name_dist_'+str(i)][j], df_dups['is_psfix_'+str(i)][j], SOUND_D_THR, NAME_D_THR, IS_PSFIX_THR) for j in range(len(df_dups)) ]
		df_dups['result_'+str(i)] = [ assign_category_outcome( df_dups['UniqueID'][j], df_dups['uid_'+str(i)][j], df_dups['cat_'+str(i)][j]) for j in range(len(df_dups)) ]

		print (df_dups['cat_'+str(i)].value_counts())
		print()
		print (df_dups['result_'+str(i)].value_counts())

	df_dups.to_csv(save_to, index=False, header=True)

# Create summary csv's for confirmed and possible duplicates
def mark_confirmed_duplicates (ids_dict, params_path_data, params_list_data, n_neighbors = 5):

	poss_dups_path = 'possible_duplicates'
	poss_dups_path += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		poss_dups_path += '_' + str(i)
	poss_dups_path += ').csv'

	load_from = poss_dups_path.replace("possible", "categories")
	save_to_conf = poss_dups_path.replace("possible", "confirmed")
	save_to_maybe = poss_dups_path.replace("possible", "maybe")

	print("Creating confirmed / maybe duplicates file...")
	print("Saving at: " + save_to_conf + " / " + save_to_maybe)
	print("Loading dataset from: " + load_from)

	df_dups = pd.read_csv(load_from, encoding="utf-8")

	dups_set = set({})
	maybe_set = set({})
	conf_dups = []
	maybe_dups = []
	for row in df_dups.itertuples(index=False):
		uuid1 = row[df_dups.columns.get_loc('UniqueID')]
		name1 = row[df_dups.columns.get_loc('name')]
		for i in range(n_neighbors):
			uuid2 = row[df_dups.columns.get_loc('uid_'+str(i))]
			name2 = row[df_dups.columns.get_loc('name_'+str(i))]
			sound_dist = row[df_dups.columns.get_loc('sound_dist_'+str(i))]
			name_dist = row[df_dups.columns.get_loc('name_dist_'+str(i))]
			is_psfix = row[df_dups.columns.get_loc('is_psfix_'+str(i))]
			cat = row[df_dups.columns.get_loc('cat_'+str(i))]
			res = row[df_dups.columns.get_loc('result_'+str(i))]
			if (res == 1) and ( (uuid1, uuid2) not in dups_set ) and ( (uuid2, uuid1) not in dups_set ):
				dups_set.add( (uuid1, uuid2) )
				conf_dups.append ([uuid1, uuid2, name1, name2, sound_dist, name_dist, is_psfix, cat, res])
			elif (res == 0) and ( (uuid1, uuid2) not in maybe_set ) and ( (uuid2, uuid1) not in maybe_set ):
				maybe_set.add( (uuid1, uuid2) )
				maybe_dups.append ([uuid1, uuid2, name1, name2, sound_dist, name_dist, is_psfix, cat, res])

	df_conf = pd.DataFrame(conf_dups, columns = ['uid_1', 'uid_2', 'name1', 'name2', 'sound_dist', 'name_dist', 'is_psfix', 'cat', 'res'])
	df_maybe = pd.DataFrame(maybe_dups, columns = ['uid_1', 'uid_2', 'name1', 'name2', 'sound_dist', 'name_dist', 'is_psfix', 'cat', 'res'])

	df_conf.to_csv(save_to_conf, index=False, header=True)
	df_maybe.to_csv(save_to_maybe, index=False, header=True)

# Manually check (play) the possible duplicates for the user to decide if they are
def check_possible_duplicates (ids_dict, params_path_data, params_list_data, local_clips_path):

	poss_dups_path = 'possible_duplicates'
	poss_dups_path += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		poss_dups_path += '_' + str(i)
	poss_dups_path += ').csv'

	load_from = poss_dups_path.replace("possible", "maybe")
	save_to_checked = poss_dups_path.replace("possible", "checked")

	print("Creating checked duplicates file...")
	print("Saving at: " + save_to_checked)
	print("Loading dataset from: " + load_from)

	if not os.path.exists(save_to_checked):
		df_checked = pd.read_csv(load_from, encoding="utf-8")
		df_checked['to_keep'] = -1
		df_checked.to_csv(save_to_checked, index=False, header=True)
	else:
		df_checked = pd.read_csv(save_to_checked, encoding="utf-8")

	pygame.init()
	to_keep = df_checked['to_keep'].tolist()
	start = df_checked[df_checked['to_keep']==-1].index.values[0]
	for i in range(start, len(df_checked)):
		df_checked.at[i,'to_keep'] = check_single_dup(ids_dict, df_checked.iloc[[i]], local_clips_path)
		df_checked.at[i,'res'] = -1 if df_checked.at[i,'to_keep']==2 else 1
		df_checked.to_csv(save_to_checked, index=False, header=True)	

# Display the information for both possible duplicate tracks
# Play an excerpt of both and take user input on whether it is duplicate
def check_single_dup (ids_dict, row, local_clips_path):
	print("------------------------------------------------------------------------")
	print('UID 0:', row['uid_1'].to_string(index=False))
	print('UID 1:', row['uid_2'].to_string(index=False))
	print()
	path_0 = get_key (row['uid_1'].to_string(index=False).strip(), ids_dict)
	path_1 = get_key (row['uid_2'].to_string(index=False).strip(), ids_dict)
	print('Path 0:', path_0)
	print('Path 1:', path_1)
	print()
	print('IS PFXIX' if row['is_psfix'].to_string(index=False).strip()=='1' else 'NOT PSFIX')
	print()
	print('Name distance:', row['name_dist'].to_string(index=False))
	print()
	print('Sound Distance:', row['sound_dist'].to_string(index=False))
	while True:
		play_songs(row['uid_1'].to_string(index=False).strip(), row['uid_2'].to_string(index=False).strip(), local_clips_path)
		keep = user_confirmation("Enter 1 to keep one song (duplicates), 2 to keep both (not duplicates), or anything else to repeat")
		if keep not in ['1', '2']:
			continue
		# TO DO: Change to automatic extraction of which to keep
		if keep == '1':
			keep = longer_path(path_0, path_1)

		return int(keep)	

# Play an excerpt of the songs with the ids
def play_songs(id1, id2, local_clips_path):
	j=0
	for idd in [id1, id2]:
		print("Playing song", j)
		pygame.mixer.music.load(os.path.join(local_clips_path, idd + '.wav' ))
		pygame.mixer.music.play()
		time.sleep(1.5)
		pygame.mixer.music.stop()
		time.sleep(0.2)
		j+=1
		# pygame.mixer.music.unload()

# Return which index has the longest path
def longer_path(p0, p1):
	p0, p1 = os.path.normpath(p0), os.path.normpath(p1)
	l0, l1 = p0.count('/'), p1.count('/')
	if l0 != l1:
		return 0 if l0>l1 else 1
	return 0 if len(p0)>len(p1) else 1

# Determine which index to keep based on the paths corresponding to each uid
def to_keep(uid_0, uid_1, ids_dict):
	return longer_path (get_key(uid_0, ids_dict), get_key(uid_1, ids_dict))

# Create song_ids csv without duplicates
# Takes the confirmed duplicates and checked duplicates files and keeps the one on the longest subpath for each pair (more information)
def no_duplicates_ids (ids_dict, params_path_data, params_list_data, local_clips_path):

	poss_dups_path = 'possible_duplicates'
	poss_dups_path += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		poss_dups_path += '_' + str(i)
	poss_dups_path += ').csv'

	load_from_confirmed = poss_dups_path.replace("possible", "confirmed")
	load_from_checked = poss_dups_path.replace("possible", "checked")
	save_to_no_duplicates = "CDS-Carlos_song_ids_no_duplicates" + poss_dups_path.replace("possible_duplicates", "")

	print("Creating no duplicates song ids file...")
	print("Saving at: " + save_to_no_duplicates)
	print("Loading datasets from: " + load_from_confirmed, load_from_checked)

	to_remove_ids = set({})
	
	df_confirmed = pd.read_csv(load_from_confirmed, encoding="utf-8")
	df_confirmed['to_keep'] = to_keep(df_confirmed['uid_1'], df_confirmed['uid_2'], ids_dict)
	df_confirmed['to_remove'] = df_confirmed['uid_1'] if df_confirmed['to_keep']==1 else df_confirmed['uid_2']
	to_remove_ids.add(df_confirmed['to_remove'].tolist())

	df_checked = pd.read_csv(load_from_checked, encoding="utf-8")
	df_checked['to_remove'] = df_checked['uid_1'] if df_checked['to_keep']==1 else (df_checked['uid_2'] if df_checked['to_keep']==0 else 'none')
	to_remove_ids.add(df_checked['to_remove'].tolist())

	return to_remove_ids
		

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
	# detect_poss_duplicates (ids_dict, params_path_data, params_list_data)

	# Mark categories for possible duplicates
	# mark_duplicate_categories(ids_dict, params_path_data, params_list_data)

	# Mark confirmed duplicate songs
	# mark_confirmed_duplicates(ids_dict, params_path_data, params_list_data)

	# Check maybe duplicate songs
	local_clips_path = '/Users/masc/Documents/Oscar/MaSC-Music-Visualization-master/middle_15/'
	check_possible_duplicates (ids_dict, params_path_data, params_list_data, local_clips_path)

