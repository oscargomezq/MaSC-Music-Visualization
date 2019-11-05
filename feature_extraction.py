import glob
import numpy as np
import os
import json
import librosa
from preprocessing import save_params, check_repeated_params

def extract_mfcc(params_list, **kwargs):

    filename = 'full_dataset'
    for i in params_list:
        filename += '_' + str(i)
    filename += '.csv'

    print(filename)
    print(kwargs)

    # y, sr = librosa.load(filename, offset = (fduration/2) - 2.5, duration = 5, sr=44100)

    # # Set the hop length; at 22050 Hz, 512 samples ~= 23ms
    # hop_length = 2205 #at 44100Hz, for 50ms use 2205 as hop_length

    # mfcc = librosa.feature.mfcc(y=y, sr=sr,  hop_length = hop_length, n_mfcc=13)

    # # Compute MFCC features for the overlapping sets
    # y_over, sr_over = librosa.load(filename, offset = (fduration/2) - 2.5 + 0.025, duration = 5, sr=44100)
    # mfcc_over = librosa.feature.mfcc(y=y_over, sr=sr_over, hop_length=hop_length, n_mfcc=13)


    # fp = open('MFCC_Merged_Repaired_experiment.csv', 'a', encoding='utf-8')
    # fp.write('\n')
    # fp.write(commas(filename))
    # fp.write(',')

    # for i in range(mfcc.shape[1]):
    #     for j in range(mfcc.shape[0]):
    #         fp.write(str(mfcc[j,i]))
    #         fp.write(',')
    #     for j in range(mfcc.shape[0]):    
    #         fp.write(str(mfcc_over[j,i]))
    #         fp.write(',')
        
    # fp.close()

def extract_spectrogram(filename):
    pass

def perform_feature_extraction(pre_path, ft_path, params_list):

    with open(os.path.join(pre_path, 'parameters_' + str(params_list[0]) + '.json'), 'r') as pre_f:
        tmp = pre_f.read()
        pre_param_dict = json.loads(tmp)

    with open(os.path.join(ft_path, 'parameters_' + str(params_list[1]) + '.json'), 'r') as ft_f:
        tmp = ft_f.read()
        ft_param_dict = json.loads(tmp)

    curr_params = {**pre_param_dict , **ft_param_dict}

    if curr_params['method'] == "mfcc":
        extract_mfcc(params_list, **curr_params)
    elif curr_params['method'] == "spectrogram":
        extract_spectrogram(params_list, **curr_params)
        

if __name__ == "__main__":
    
    # Need to be absolute paths (start with '/')
    # Assumes Mac connected to the CDS-Carlos server (might need to modify server_path for Windows)
    server_path = "/Volumes/CDS-Carlos"
    local_path = "/Users/masc/Documents/Oscar/MaSC-Music-Visualization-master/Server_Copy"

    # Local folders for preprocessing parameters
    preproc_params_path = 'preprocessing'
    feature_ext_params_path = 'full_datasets'

    # Define possible parameters for feature extraction
    # for method in ['mfcc', 'spectrogram']:
    #     for duration in [5, 10]:
    #         save_params(feature_ext_params_path, method = method, duration = duration)
    
    # Define a set of preprocessing parameters and a set of feature extraction parameters to use
    preproc_params = 4
    feature_ext_params = 1

    perform_feature_extraction(preproc_params_path, feature_ext_params_path, [preproc_params, feature_ext_params])


