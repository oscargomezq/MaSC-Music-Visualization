import pandas as pd
from utils import *
import shutil


ids_dict = init_unique_id_dict ('CDS-Carlos_song_ids.csv')


def n2id (name):
	name = name.replace("./EastAfricanClips/", "2_EastAfricanArchive/FINAL_East African Popular Music Archive/")
	name = name.replace("new_collection/0_NEW STUFF/", "1_NEW STUFF/")
	name = name.replace("./Clips/", "")
	name = name.replace("~", ",")
	name = name[:-4]
	# print(name)
	key = 0
	try:
		key = get_id(name, ids_dict)
	except:
		with open ('3D_VR_Error_Log.txt', 'a', encoding='utf-8') as error_log:
			error_log.write(name + '\n')
	return key


def middle_15_upload():
	coord_df = pd.read_csv('3d_coordinates_VR_new.csv', encoding='utf-8')
	id_list = coord_df.values[:,0]
	print(id_list)
	
	for uid in id_list:
		path_from = os.path.join('middle_15', uid + '.wav')
		path_to = os.path.join('middle_15_up', uid + '.wav')
		if (not os.path.exists(path_to)) and uid!='0':
			try:
				shutil.copy(path_from, path_to)
			except:
				with open ('copy_mid15_eror_log.txt', 'a', encoding='utf-8') as error_log:
					error_log.write(path_from + '\n')


# coord_df = pd.read_csv('3d_coordinates_VR.csv', encoding='utf-8')

# coord_df['Name'] = coord_df['Name'].apply(n2id)
# print(coord_df.head())

# coord_df.to_csv('3d_coordinates_VR_new.csv', index=False)

middle_15_upload()
