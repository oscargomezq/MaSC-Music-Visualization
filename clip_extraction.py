import glob
import numpy as np
import os
import librosa
from os.path import join, getsize


def process(jfilename):
    
    out = "EastAfricanClips" + jfilename[1:]
    # print (out)
    pos = 0
    for i in range(len(out)):
        if out[i] == '/':
            pos = i
    out2 = out[:pos]
    for i in range(len(out)):
        if out[i] == '.':
            pos = i
    out3 = out[:pos] + ".wav"
    print (out3)

    if not os.path.exists(out2):
    	fduration = librosa.get_duration(filename=jfilename)
    	y, sr = librosa.load(jfilename, offset = (fduration/2) - 7.5, duration = 15, sr=44100)
    	os.makedirs(out2)
    	librosa.output.write_wav(out3, y, sr)

    else:
    	fduration = librosa.get_duration(filename=jfilename)
    	y, sr = librosa.load(jfilename, offset = (fduration/2) - 7.5, duration = 15, sr=44100)
    	librosa.output.write_wav(out3, y, sr)



for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        k = os.path.join(root, name)
        pos = 0
        for i in range(len(k)):
            if (k[i]=='.'):
                pos = i
        j = k[pos:]

        if (j == ".aiff" or j == ".wav" or j == ".WAV" or j == ".aif"):
            process(k)
            # if (k == "./New CDs - Emma /Wa7dek/1 Allah Alalim.aiff"):
            #     print(k)
            #     process(k)

