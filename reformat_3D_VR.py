import pandas as pd
from utils import *



ids_dict = init_unique_id_dict ('CDS-Carlos_song_ids.csv')


def n2id (name):
	name = name.replace("./EastAfricanClips/", "")
	name = name.replace("./Clips/", "")
	name = name.replace("~", ",")
	name = name[:-4]
	# print(name)
	key = 0
	try:
		key = get_key(name, ids_dict)
	except:
		with open ('3D_VR_Error_Log.txt', 'a', encoding='utf-8') as error_log:
			error_log.write(name + '\n')
	return key




coord_df = pd.read_csv('3d_coordinates_VR.csv', encoding='utf-8')

n = coord_df.iloc[0,0]
print(n)
print(n2id(n))


coord_df['Name'] = coord_df['Name'].apply(n2id)
print(coord_df.head())

coord_df.to_csv('3d_coordinates_VR_new.csv', index=False)

# with open('3d_coordinates_VR.csv', 'r', encoding='utf-8') as 3d_file:
