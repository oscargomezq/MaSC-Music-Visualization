import glob
import numpy as np
import os
import librosa
from os.path import join, getsize
from librosa import display
import matplotlib.pyplot as plt
from librosa import power_to_db

def process(filename):
    
	# Load the example clip
	fduration = librosa.get_duration(filename=filename[2:])

	y, sr = librosa.load(filename, offset = (fduration/2) - 2.5, duration = 5, sr=44100)#44100

	# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
	hop_length = 2205 #2205 #at 44100Hz, for 50ms use 2205 as hop_length

	S = np.abs(librosa.stft(y, hop_length=hop_length))

	log_S = librosa.power_to_db(S**2)

	fp = open('Log_Mel_Spectrogram_Merged_Repaired_experiment.csv', 'a', encoding='utf-8')
	fp.write('\n')
	fp.write(commas(filename))
	fp.write(',')

	print (log_S.shape)

	for i in range(log_S.shape[0]):
	    
	    for j in range(log_S.shape[1]):

	    	fp.write(str(log_S[i][j]))
	    	fp.write(',')

	fp.close()

def commas (filename):
    name = filename
    return name.replace(",", "~")


# for root, dirs, files in os.walk(".", topdown=False):
#     for name in files:
#         k = os.path.join(root, name)
#         pos = 0
#         for i in range(len(k)):
#             if (k[i]=='.'):
#                 pos = i
#         j = k[pos:]
#         if (j == ".wav" and k!= './New CDs - Emma /Songs Of The Pashaï/3 I Beseech You, Do Not Spend Your Life.wav'):
#         	print(k)
#         	process(k)

# DONT INCLUDE TRYOUT!!!

# for root, dirs, files in os.walk(".", topdown=False):
#     for name in files:
#         k = os.path.join(root, name)
#         pos = 0
#         for i in range(len(k)):
#             if (k[i]=='.'):
#                 pos = i
#         j = k[pos:]
#         if (k[2] != 'S' and j == ".wav" and ("Clips/Tryout/new_collection/0_NEW STUFF" in k)): #and k!= './New CDs - Emma /Songs Of The Pashaï/3 I Beseech You, Do Not Spend Your Life.wav'):
#         	print(k)
#         	# process(k)

# k = './EastAfricanClips/New CDs - Emma /Songs Of The Pashaï/3 I Beseech You, Do Not Spend Your Life.wav'
# process(k)
i=0
for root, dirs, files in os.walk('.'):
    p = root
    for name in files:
    	k =  (p+'/'+name)
    	if ((k[2:9] != 'Scripts') and (k[2:18] != 'EastAfricanClips') and ((".wav" in k) or (".aif" in k)) and ("experiment" in k)):# and (k!= './EastAfricanClips/New CDs - Emma /Songs Of The Pashaï/3 I Beseech You, Do Not Spend Your Life.wav')):
            print(k)
            # process(k)
            i+=1
print(i)

# fp = open('Log_Mel_Spectrogram_Merged_Repaired_All_v2.csv', 'r', encoding='utf-8')
# fp1 = open('Log_STFT_Merged_Repaired_All_v2.csv', 'w', encoding='utf-8')

# j=0
# row = fp.readline()
# j+=1
# while row:
#     row = fp.readline()
#     if j>=2895:
#     	# print(len(row.split(',')))
#     	fp1.write(row)
#     j+=1

# fp1.close()
# fp.close()











