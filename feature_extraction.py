import glob
import numpy as np
import pandas as pd
import os
import json
import librosa
from preprocessing import save_params, check_repeated_params

# Extract all the mfccs from the audio files in audio_path to the save_to_path directory
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def extract_mfcc(save_to_path, audio_path, **kwargs):
    
    mfcc_arr = []
    for root, dirs, files in os.walk(audio_path):
        progress = 0
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if file_extension in ['.wav']:

                d = kwargs
                full_duration = librosa.get_duration(filename=filedir)

                # Compute MFCC features for the first sets
                y, sr = librosa.load(filedir, offset = (full_duration/2) - d['duration']/2, duration = d['duration'], sr = d['sr'])
                mfcc = librosa.feature.mfcc(y=y, sr=sr,  hop_length=d['hop_length'], n_mfcc=13)

                # Compute MFCC features for the overlapping sets
                y_over, sr_over = librosa.load(filedir, offset = (full_duration/2) - 2.5 + d['window_size']/2000, duration = d['duration'], sr = d['sr'])
                mfcc_over = librosa.feature.mfcc(y=y_over, sr=sr_over, hop_length=d['hop_length'], n_mfcc=13)

                unique_id, _ = os.path.splitext(name)

                row = [unique_id]
                row.extend(np.ravel(mfcc))
                row.extend(np.ravel(mfcc_over))
                mfcc_arr.append(row)
                progress += 1
                if progress%100 == 0:
                    print("Processed", progress, "/", len(files))

    mfcc_arr = pd.DataFrame(mfcc_arr)
    print(mfcc_arr)
    mfcc_arr.to_csv(save_to_path, index=False, header=False)


def extract_spectrogram(filename):
    pass

# Perform feature extraction on the audio files in audio_path
# pre_path is the path where the preprocessing parameters are stored
# ft_path is the path where the feature extraction parameters are stored
# params list is the combination of parameters to be used for this step
def perform_feature_extraction(pre_path, ft_path, params_list, audio_path):

    save_to = 'full_dataset'
    for i in params_list:
        save_to += '_' + str(i)
    save_to += '.csv'
    save_to = os.path.join(ft_path, save_to)

    with open(os.path.join(pre_path, 'parameters_' + str(params_list[0]) + '.json'), 'r') as pre_f:
        tmp = pre_f.read()
        pre_param_dict = json.loads(tmp)

    with open(os.path.join(ft_path, 'parameters_' + str(params_list[1]) + '.json'), 'r') as ft_f:
        tmp = ft_f.read()
        ft_param_dict = json.loads(tmp)

    curr_params = {**pre_param_dict , **ft_param_dict}

    print("Performing feature extraction...")
    print("Using parameters: " + str(curr_params))
    print("Saving at: " + save_to)

    # Extract features for a clip using the preferred parameters
    if curr_params['method'] == "mfcc":
        extract_mfcc(save_to, audio_path, **curr_params)
    elif curr_params['method'] == "spectrogram":
        extract_spectrogram(save_to, audio_path, **curr_params)

    
        

if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'

    # Define possible parameters for feature extraction
    for method in ['mfcc', 'spectrogram']:
        for duration in [5, 10]:
            save_params(feature_ext_path, method=method, duration=duration)
    
    # Define a set of preprocessing parameters and a set of feature extraction parameters to use
    preproc_params = 2
    feature_ext_params = 1

    # Define the audio clips to be used
    audio_path = 'middle_15'

    perform_feature_extraction(preproc_path, feature_ext_path, [preproc_params, feature_ext_params], audio_path)


