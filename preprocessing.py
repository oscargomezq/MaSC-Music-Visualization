import glob
import os
import json


# Define the preprocessing parameters for the experiment
# Saved in the params_root directory as a JSON file
# Check against previously defined sets of parameters to avoid repetition
def save_params (params_root, **kwargs):
    param_dict = kwargs
    repeated, idx = check_repeated_params(params_root, param_dict)
    print("Parameters already defined at " + idx if repeated else 'Saving new parameters at parameters_' + str(idx))
    if not repeated:
        with open(os.path.join(params_root, 'parameters_' + str(idx) + '.json'), 'w') as f:
            json.dump(param_dict, f, sort_keys=True)

# If the parameters are repeated, the first return value is True, else it is False
# If the parameters are repeated, the second return value is the file where the repetition occurs, else it is the next usable index to store parameters
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
                        return True, filedir
                    next_idx += 1
    return False, next_idx


if __name__ == "__main__":

    # Local folder for preprocessing parameters
    preproc_params_path = 'preprocessing'

    # Define possible parameters for preprocessing
    param_set_1 = {'sr': 22050, 'window_size': 23, 'hop_length': 512}
    param_set_2 = {'sr': 44100, 'window_size': 50, 'hop_length': 2205}
	# Set the hop length; at 22050 Hz, 512 samples ~= 23ms  # at 44100Hz, for 50ms use 2205 as hop_length

    save_params(preproc_params_path, **param_set_1)
    save_params(preproc_params_path, **param_set_2)

