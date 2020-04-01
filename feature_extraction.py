import numpy as np
import pandas as pd
import os
import librosa
from utils import save_params, check_repeated_params, unpack_params, song_subset

# Extract all the mfccs from the audio files in audio_path to the save_to_path directory
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def extract_mfcc (ids_dict, save_to_path, audio_path, **kwargs):
    
    d = kwargs
    mfcc_arr = []

    s_subset = song_subset(audio_path, server_subpaths=d['server_subpaths'], ids_dict=ids_dict)
    progress = 0
    for unique_id, filedir in s_subset:

        full_duration = librosa.get_duration(filename=filedir)

        # Compute MFCC features for the first sets
        y, sr = librosa.load(filedir, offset = (full_duration/2) - d['duration']/2, duration = d['duration'], sr = d['sr'])
        mfcc = librosa.feature.mfcc(y=y, sr=sr,  hop_length=d['hop_length'], n_mfcc=13)

        # Compute MFCC features for the overlapping sets
        y_over, sr_over = librosa.load(filedir, offset = (full_duration/2) - 2.5 + d['window_size']/2000, duration = d['duration'], sr = d['sr'])
        mfcc_over = librosa.feature.mfcc(y=y_over, sr=sr_over, hop_length=d['hop_length'], n_mfcc=13)

        row = [unique_id]
        row.extend(np.ravel(mfcc))
        row.extend(np.ravel(mfcc_over))
        mfcc_arr.append(row)
        progress += 1
        if progress%100 == 0:
            print("Processed", progress, "/", len(s_subset))

    mfcc_arr = pd.DataFrame(mfcc_arr)
    mfcc_arr.to_csv(save_to_path, index=False, header=False)

# Extract the spectrogram from the audio files in audio_path to the save_to_path directory
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def extract_spectrogram (save_to_path, audio_path, **kwargs):

    d = kwargs
    spect_arr = []

    s_subset = song_subset(audio_path, server_subpaths=d['server_subpaths'], ids_dict=ids_dict)
    progress = 0
    for unique_id, filedir in s_subset:

        full_duration = librosa.get_duration(filename=filedir)

        # Compute Spectogram STFT features
        y, sr = librosa.load(filedir, offset = (full_duration/2) - d['duration']/2, duration = d['duration'], sr = d['sr'])
        S = np.abs(librosa.stft(y, hop_length=d['hop_length']))
        log_S = librosa.power_to_db(S**2)

        row = [unique_id]
        row.extend(np.ravel(log_S))
        spect_arr.append(row)
        progress += 1
        if progress%100 == 0:
        	print("Processed", progress, "/", len(s_subset))
        	spect_arr = pd.DataFrame(spect_arr)
        	spect_arr.to_csv(save_to_path, index=False, header=False, mode='a')
        	spect_arr = []


# Perform feature extraction on the audio files in audio_path
# ids_dict is the dictionary to retrieve original filenames from the Unique-ID
# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params list is the combination of parameters to be used for this step
# audio_path is the folder of clips to use (eg. middle_15)
def perform_feature_extraction (ids_dict, params_path, params_list, audio_path):

    save_to = 'full_dataset'
    for i in params_list:
        save_to += '_' + str(i)
    save_to += '.csv'
    save_to = os.path.join(params_path[-1], save_to)

    curr_params = unpack_params(params_path, params_list)

    print("Performing feature extraction...")
    print("Using parameters: " + str(curr_params))
    print("Saving at: " + save_to)

    if os.path.exists(save_to):
        print ("Feature extraction for these parameters already done!")
        return

    # Extract features for a clip using the preferred parameters
    if curr_params['method'] == "mfcc":
        extract_mfcc(ids_dict, save_to, audio_path, **curr_params)
    elif curr_params['method'] == "spectrogram":
        extract_spectrogram(save_to, audio_path, **curr_params) 
        

if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    params_path = [preproc_path, feature_ext_path]

    # Define possible parameters for feature extraction
    for method in ['mfcc', 'spectrogram']:
        for duration in [5, 10]:
            save_params(feature_ext_path, method=method, duration=duration, random_state=0)
    
    # Define a set of preprocessing parameters and a set of feature extraction parameters to use
    preproc_params = 3
    feature_ext_params = 3
    params_list = [preproc_params, feature_ext_params]

    # Define the audio clips to be used
    audio_path = 'middle_15'

    # Initialize the key - id dictionary
    from utils import init_unique_id_dict
    ids_dict = init_unique_id_dict('CDS-Carlos_song_ids.csv')

    perform_feature_extraction(ids_dict, params_path, params_list, audio_path)


