import os
import json
from create_ids import get_id
from preprocessing import save_params, check_repeated_params

# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params list is the combination of parameters to be used for this step
def unpack_params (param_paths, params_list):

	curr_params = {}
	for i in range(len(params_list)):
	    with open(os.path.join(param_paths[i], 'parameters_' + str(params_list[i]) + '.json'), 'r') as param_f:
	        tmp = param_f.read()
	        curr_params.update(json.loads(tmp))
	return curr_params
