import os
import uuid

# Assign each song in the server a Unique ID to use for the analysis
# The ID is generated exclusively from the original folder structure in the server
# See https://stackoverflow.com/a/51550196
# We used a base ID (generated with uuid1) that defines our custom namespace
def assign_unique_ids (server_root_path, audio_formats, ids_csv_path):

    print("Assigning Unique IDs...")
    if os.path.exists(ids_csv_path):
        print ("Unique IDs already created at " + ids_csv_path + "!")
        return
    for root, dirs, files in os.walk(server_root_path):
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if file_extension in audio_formats:
                l_root = root.replace(server_root_path+'/', '') # Remove the server_root_path from local copy
                l_root = l_root.replace(server_root_path, '') # For first children of server_root_path
                path_for_id = os.path.join(l_root, name)
                id_key = os.path.splitext(path_for_id)[0] # Remove extension for ID generation
                # Assign unique ID
                unique_id = get_id(id_key)
                with open(ids_csv_path, 'a', encoding='utf-8') as ids_file:
                    ids_file.write(str(unique_id) + "," + "\"" + id_key + "\"" + "\n") # Enclose audio path in " " for handling commas and quotes within filepaths

# Get Unique ID from string
# Tne string id_key must be the path in the CDS-Carlos server, without /Volumes/CDS-Carlos/ and without the file extension
# The BASE_ID must be the one provided below for reproducibility!
# BASE_ID: 942f26ce-fa3e-11e9-a5be-685b35c80712
def get_id (id_key):
    # DO NOT CHANGE, generated on OCT 29 / 2019 on CDS Computer
    BASE_ID = uuid.UUID('{942f26ce-fa3e-11e9-a5be-685b35c80712}')
    unique_id = uuid.uuid5(BASE_ID, id_key)
    return unique_id


# Formats to consider for making a local copy (music and cover art)
aud_formats = set(['.wav', '.m4a', '.WAV', '.aiff', '.aif'])
img_formats = set(['.tif', '.jpg', '.JPG', '.png'])

if __name__ == "__main__":
    
    # Need to be absolute paths (start with '/')
    # Assumes Mac connected to the CDS-Carlos server (might need to modify server_path for Windows)
    server_path = "/Volumes/CDS-Carlos"
    local_path = "/Users/masc/Documents/Oscar/MaSC-Music-Visualization-master/Server_Copy"

    assign_unique_ids(server_path, aud_formats, 'CDS-Carlos_song_ids.csv')
