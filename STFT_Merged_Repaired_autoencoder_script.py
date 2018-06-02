import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from keras.layers import Input, Dense, Lambda, Layer
from keras.models import Model
from keras import backend as K
from keras import metrics
from sklearn.decomposition import PCA

fp = open ('Log_STFT_Merged_Repaired_All_v2.csv', 'r', encoding='utf-8')

names = []
samples = 2972
features = 1025*101
x_train = np.zeros((samples-1,features))

# fp.readline()

for i in range(samples):
    row = fp.readline().split(',')
    if ('Clips/Roubaiyat El Khayam/15 Wasla in Dugah_ Quatrains 309~ 247~ 297~ 290 and 80.wav' in row[0]):
        continue 
    names.append(row[0])
    for j in range (features):
        try:
            x_train[i][j] = float(row[j+1])
        except:
            # print(',',row[j+1],',')
            # print(i,j)               
            break

fp.close()
print('initial reading done')

# features = 2000

# pca = PCA(n_components=features)
# x_train = pca.fit_transform(x_train)

# print(x_train.shape)
# print(np.sum(pca.explained_variance_ratio_))

x_train = x_train / x_train.min()
# find_max = np.amax([np.amax(x_train), np.amin(x_train)])
# print (np.amax(x_train), np.amin(x_train))

# x_train = x_train.astype('float32') / find_max
# print(x_train.shape)
# x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
# print(x_train.shape)

# noise_factor = 0.5
# x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape) 

# x_train_noisy = np.clip(x_train_noisy, 0., 1.)

encoding_dim = 50
input_img = Input(shape=(features,))

# # encoded = Dense(8192, activation='relu')(input_img)
# # encoded = Dense(4096, activation='relu')(encoded)
# # encoded = Dense(2048, activation='relu')(encoded)
# # encoded = Dense(1024, activation='relu')(input_img)
encoded = Dense(2000, activation='relu')(input_img)
encoded = Dense(100, activation='relu')(encoded)
encoded = Dense(50, activation='relu')(encoded)
# encoded = Dense(500, activation='relu')(encoded)

decoded = Dense(100, activation='relu')(encoded)
decoded = Dense(2000, activation='relu')(decoded)
# decoded = Dense(5000, activation='relu')(decoded)
# # decoded = Dense(1024, activation='relu')(decoded)
# # decoded = Dense(2048, activation='relu')(decoded)
# # decoded = Dense(4096, activation='relu')(decoded)
# # decoded = Dense(8192, activation='relu')(decoded)
decoded = Dense(features, activation='sigmoid')(decoded) #activation='tanh' , 'sigmoid'

autoencoder = Model(input_img, decoded)
#autoencoder.summary()

encoder = Model(input_img, encoded)

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_split = 0.2)


outfilename = '50d_Merged_Repaired_no_dups_STFT_autoencoder_try1.csv'
fp = open(outfilename, 'w', encoding='utf-8')

encoded_audios = encoder.predict(x_train)

for i in range(10):
    print(encoded_audios[i])

for i in range (samples-1):
    fp.write(names[i])
    fp.write(',')
    for j in range(encoding_dim):#encoding_dim
        fp.write(str(encoded_audios[i][j]))#encoded_audios[i][j])
        fp.write(',')
    fp.write('\n')
fp.close()

# # build a digit generator that can sample from the learned distribution
# decoder_input = Input(shape=(latent_dim,))
# _h_decoded = decoder_h(decoder_input)
# _x_decoded_mean = decoder_mean(_h_decoded)
# generator = Model(decoder_input, _x_decoded_mean)
