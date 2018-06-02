import glob
import numpy as np
import os
import librosa
from os.path import join, getsize

def process(filename):
    
    # Load the example clip
    fduration = librosa.get_duration(filename=filename[2:])

    y, sr = librosa.load(filename, offset = (fduration/2) - 2.5, duration = 5, sr=44100)

    # Set the hop length; at 22050 Hz, 512 samples ~= 23ms
    hop_length = 2205 #at 44100Hz, for 50ms use 2205 as hop_length

    mfcc = librosa.feature.mfcc(y=y, sr=sr,  hop_length = hop_length, n_mfcc=13)

    # Compute MFCC features for the overlapping sets
    y_over, sr_over = librosa.load(filename, offset = (fduration/2) - 2.5 + 0.025, duration = 5, sr=44100)
    mfcc_over = librosa.feature.mfcc(y=y_over, sr=sr_over, hop_length=hop_length, n_mfcc=13)


    fp = open('MFCC_Merged_Repaired_experiment.csv', 'a', encoding='utf-8')
    fp.write('\n')
    fp.write(commas(filename))
    fp.write(',')

    for i in range(mfcc.shape[1]):
        for j in range(mfcc.shape[0]):
            fp.write(str(mfcc[j,i]))
            fp.write(',')
        for j in range(mfcc.shape[0]):    
            fp.write(str(mfcc_over[j,i]))
            fp.write(',')
        
    fp.close()

def commas (filename):
    name = filename
    return name.replace(",", "~")


# fp = open('MFCC_Merged_Repaired_All.csv', 'a', encoding='utf-8')

# fp.write('\n')

# fp1 = open('MFCC_Merged_no_dups_All.csv', 'r', encoding='utf-8')

# samples = 2271
# roww = fp1.readline().split(',')

# for i in range(samples):

#     roww = fp1.readline()
#     fp.write(roww)

# fp1.close()

# fp.close()
i = 0
for root, dirs, files in os.walk('.'):
    p = root
    for name in files:
        k =  (p+'/'+name)
        if ((k[2:9] != 'Scripts') and (k[2:18] != 'EastAfricanClips') and ((".wav" in k) or (".aif" in k)) and ('experiment' in k)):
            print(k)
            i+=1
            process(k)
print (i)
                    
