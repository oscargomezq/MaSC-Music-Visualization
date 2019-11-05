import glob
import os
import json


# Define the preprocessing parameters for the experiment
# Saved in the /preprocessing_parameters directory as a JSON file
# Check against previously defined sets of parameters to avoid repetition
def save_params (params_root, **kwargs):
    param_dict = kwargs
    idx = check_repeated_params(params_root, param_dict)
    print("Parameters already defined" if idx==0 else 'parameters_' + str(idx))
    if idx > 0:
        with open(os.path.join(params_root, 'parameters_' + str(idx) + '.json'), 'w') as f:
            json.dump(param_dict, f, sort_keys=True)

# Returns 0 if parameters are repeated, or the next usable index of the parameters defined otherwise
def check_repeated_params (params_root, param_dict):
    for root, dirs, files in os.walk(params_root):
        next_idx = 1
        for name in files:
            filedir = os.path.join(root, name)
            filename, file_extension = os.path.splitext(filedir)
            if (file_extension == '.json'):
                with open(filedir, 'r') as json_f:
                    tmp = json_f.read()
                    if param_dict == json.loads(tmp):
                        return 0
                    next_idx += 1
    return next_idx


if __name__ == "__main__":
    
    # Need to be absolute paths (start with '/')
    # Assumes Mac connected to the CDS-Carlos server (might need to modify server_path for Windows)
    server_path = "/Volumes/CDS-Carlos"
    local_path = "/Users/masc/Documents/Oscar/MaSC-Music-Visualization-master/Server_Copy"

    # Local folder for preprocessing parameters
    preproc_params_path = 'preprocessing'

    for sr in [22050, 44100]:
        for hop_length in [512,2205]:
            save_params(preproc_params_path, hop_length = hop_length, sr = sr)

