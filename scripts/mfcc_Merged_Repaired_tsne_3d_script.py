import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from bokeh.layouts import row, gridplot, layout
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, TapTool, WheelZoomTool, LassoSelectTool, BoxSelectTool, PanTool, HelpTool
from bokeh.plotting import figure, output_file, show
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_artist(name):

	## Clips

	if (name[2] == 'C'):

		if ('Compilations' in name):
			start = name.find('tions') + 6
			end = name[start:].find('/')
			return name[start:start+end]

		elif ('new_collection' in name):
			start = name.find('FF') + 3
			end = name[start:].find('/')
			return name[start:start+end]

		elif ('Various Artists' in name):
			start = name.find('Artists') + 8
			end = name[start:].find('/')
			return name[start:start+end]

		else:
			start = 8
			end = name[start:].find('/')
			return name[start:start+end]


	else:

		## EastAfricanClips

		if ('from Jamal' in name):
			start = name.find('Hafidh') + 7
			end = name[start:].find('/')
			return "EAST AFRICAN " + name[start:start+end]

		elif ('from Prahbo' in name):
			start = name.find('Patel') + 6
			end = name[start:].find('/')
			return "EAST AFRICAN " + name[start:start+end]

		elif ('Bonzo &' in name):
			return "EAST AFRICAN " + 'Bonzo & Party'

		elif ('Zein Musical Party' in name):
			return "EAST AFRICAN " + 'Zein Musical Party Vol 10'

		# elif ('Emma' in name):
		# 	start = name.find('Emma') + 5
		# 	print (start)
		# 	end = name[start:].find('/')
		# 	return name[start:start+end]

		else:
			start = name.find('Emma') + 6
			end = name[start:].find('/')
			return "EAST AFRICAN " + name[start:start+end]

filename = 'MFCC_Merged_Repaired_All_v2.csv'
fp = open(filename, 'r', encoding='utf-8')

samples = 2792 
features = 2627

X = np.zeros((samples,features))
names = []
artists = []
proper_names = []
display_names = []

roww = fp.readline().split(',')
for i in range(samples+1): #add one for break

    roww = fp.readline().split(',')

    if(len(roww)>3):
    	names.append(roww[0])
    	artists.append(get_artist(roww[0]))
    	for j in range (features):
    		try:
    			v = float(roww[j+1])
    			X[i][j] = v
    		except:
    			break

print(len(names))

for i in range(samples):
    proper_names.append(names[i].replace("~",","))
    cnt = 0
    for j in range(len(proper_names[i])):
        if proper_names[i][j] == "/":
            cnt = j
    display_names.append(proper_names[i][cnt+1:])

print('initial reading done')
fp.close()

scaler = StandardScaler()
X = scaler.fit_transform(X)
print(scaler.mean_.shape)
print(scaler.n_samples_seen_)

####### KMeans #######
min_inertia = 10**20
fk = 6
labels = []
xp = range(1,20)
yp = []
for k in [6]:
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    tlabels = kmeans.labels_
    inertia = kmeans.inertia_
    yp.append(inertia)
    print (k, inertia)
    if inertia < min_inertia:
        min_inertia = inertia
        fk = k
        labels = tlabels
print('kmeans done', fk, "clusters")

color_opt = ["olive", "darkred", "goldenrod", "skyblue", "red", "darkblue", "gray", "indigo", "black"]
colors = []
for k in range(len(proper_names)):
    colors.append(color_opt[labels[k]])

######################


################# Fast initial reading #########################
# filename = '2d_Merged_Repaired_no_dups_mfcc_tsne_prx_10_l-rate_2000_try_6_v2.csv'
# fp = open(filename, 'r', encoding='utf-8')
# samples = 2792 
# names = []
# artists = []
# proper_names = []
# display_names = []
# for i in range(samples): #add one for break
#     roww = fp.readline().split(',')
#     names.append(roww[0])
#     artists.append(get_artist(roww[0]))
# print(len(names))
# for i in range(samples):
#     proper_names.append(names[i].replace("~",","))
#     cnt = 0
#     for j in range(len(proper_names[i])):
#         if proper_names[i][j] == "/":
#             cnt = j
#     display_names.append(proper_names[i][cnt+1:])
# print('initial reading done')
# fp.close()
################################################################


newartists = list(set(artists))
newartists.sort()

for p in range(1,2):

    prx = 30
    l_rate = 200

    # model = TSNE(n_components=3, perplexity=prx, learning_rate=l_rate, n_iter=5000)#, init='pca'
    # np.set_printoptions(suppress=True)
    # T = model.fit_transform(X)
    # print (T.shape)
    # print (model.kl_divergence_)

    fp = open('3d_Merged_Repaired_no_dups_mfcc_tsne_prx_' + str(prx) + '_l-rate_' + str(l_rate) + '_try_' + str(p) +'_v2stdscale_cols.csv', 'w', encoding='utf-8')
    for i in range (samples):
        fp.write(names[i])
        fp.write(',')
        # x.append(T[i][0])
        # y.append(T[i][1])
        # z.append(T[i][2])
        # fp.write(str(T[i][0]))
        # fp.write(',')
        # fp.write(str(T[i][1]))
        # fp.write(',')
        # fp.write(str(T[i][2]))
        # fp.write(',')
        fp.write(str(colors[i]))
        fp.write('\n')

    fp.close()

    