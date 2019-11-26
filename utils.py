import os
import json
import pandas as pd
from create_ids import get_id, get_key, init_unique_id_dict
from preprocessing import save_params, check_repeated_params, song_subset

# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params list is the combination of parameters to be used for this step
def unpack_params (param_paths, params_list):

	curr_params = {}
	for i in range(len(params_list)):
	    with open(os.path.join(param_paths[i], 'parameters_' + str(params_list[i]) + '.json'), 'r') as param_f:
	        tmp = param_f.read()
	        curr_params.update(json.loads(tmp))
	return curr_params

def user_confirmation(msg=None):
	print()
	if msg==None:
		inp = input("Enter 'q' to quit or any other key to continue: ")
	else:
		inp = input(msg + "\nor enter 'q' to quit: ")
	print()
	if inp == 'q':
		sys.exit()
	else:
		return inp
