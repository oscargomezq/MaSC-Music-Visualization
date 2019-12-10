import os
import numpy as np
import pandas as pd

def artist_input():
    

# Assign each song in the server an artist to use for the analysis
# Prompts the user to assign an artist selected from one of the subfolders in the path
def assign_artist (group_arr):

    all_subfolders = os.path.normpath(group_arr[0][1]).split(os.path.sep)
    print()
    print ("Enter number for the artist:")
    for i in range(len(all_subfolders)):
        print (i, "---", all_subfolders[i])
    print("NA", "---", "Enter artist manually")
    print()

    artist_idx = input("Number or 'NA': ")
    if artist_idx == "NA":
        artist = input("Please enter artist name for this group: ")
    else:
        try:
            artist = all_subfolders[int(artist_idx)]
        except:


    print(artist)
    print()
    return group_arr

# Go through all the IDs and assign metadata to each leaf subfolder (By album or more granular)
def perform_metadata_input (ids_csv_path, save_to):

    # Open IDs file
    ids_df = pd.read_csv(ids_csv_path, header=None, encoding='utf-8')
    ids_arr = ids_df.values
    group_cnt = 0

    idx = 0
    leaf_dir = os.path.normpath(ids_arr[0][1]).split(os.path.sep)[-2]
    for i in range(1,ids_arr.shape[0]):
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
            group_with_artist = assign_artist(group)

            # Calls to other methods
            # Updated dataframe returned

            # Append to the corpus_statistics file
            with open(save_to, 'a', encoding='utf-8') as stats_file:
                for row in group_with_artist:
                    pass
                    # print(row)

                    # stats_file.write()
                print(leaf_dir)
                print("Songs in this group:", group_with_artist.shape[0])
                print("------------------------------")

            idx = i
            leaf_dir = curr_leaf
            group_cnt += 1

    print()
    print("Total leaf groups: " + group_cnt)



if __name__ == "__main__":
    
    # Path to save the file that contains all metadata
    metadata_path = "corpus_statistics.csv"

    perform_metadata_input('CDS-Carlos_song_ids.csv', metadata_path)
