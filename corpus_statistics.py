import os
import numpy as np
import pandas as pd

def artist_input():
    pass

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
            	# arr_str = np.array2string(group_update, separator=',')
            	# arr_str = ''.join(arr_str.split())
            	# arr_str = arr_str[2:-2] + '\n'
            	# arr_str = arr_str.replace('[','').replace('],','\n')
            	# arr_str = arr_str.replace('\'','\"')
            	# stats_file.write(arr_str)

            print(leaf_dir)
            print("Songs in this group:", group_update.shape[0])
            print("------------------------------")

            idx = i
            leaf_dir = curr_leaf
            group_cnt += 1

    print()
    print("Total leaf groups:", group_cnt)



if __name__ == "__main__":
    
    # Path to save the file that contains all metadata
    metadata_path = "corpus_statistics.csv"

    perform_metadata_input('CDS-Carlos_song_ids.csv', metadata_path)
