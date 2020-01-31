import os
import numpy as np
import pandas as pd
from sklearn import metrics


# Calculate cluster purity
def cluster_purity (ground_labels, assigned_labels):

    return group_arr


# Calculate cluster accuracy
def cluster_accuracy (ground_labels, assigned_labels):

    return group_arr


# Calculate cluster entropy
def cluster_entropy (ground_labels, assigned_labels):

    return group_arr


# Calculate cluster rand score
def cluster_rand_score (ground_labels, assigned_labels):
    score = metrics.adjusted_rand_score(ground_labels, assigned_labels)
    return score



if __name__ == "__main__":
    
    # Paths that contain the data and cluster assignments
    mfcc_data_path = "replicate_2d_Merged_Repaired_no_dups_mfcc_tsne_prx_30_l-rate_200_try_1_v2stdscale.csv"
    stft_data_path = "replicate_50d_Merged_Repaired_no_dups_STFT_autoencoder_try1_tsne_prx_30_l-rate_200_try_1_stdscale1.csv"

    # Read labels
    mfcc_df = pd.read_csv("replicate_2d_Merged_Repaired_no_dups_mfcc_tsne_prx_30_l-rate_200_try_1_v2stdscale.csv",
                           header=None, encoding='utf-8')

    stft_df = pd.read_csv("replicate_50d_Merged_Repaired_no_dups_STFT_autoencoder_try1_tsne_prx_30_l-rate_200_try_1_stdscale1.csv",
                           header=None, encoding='utf-8')

    # Flip 2-means labels for MFCC
    mfcc_df.iloc[:,5] = [(1 if x==0 else 0) for x in mfcc_df.iloc[:,5].values]

    # Ground truth labels
    mfcc_ground_labels = mfcc_df.values[:,4]    # 2972
    stft_ground_labels = stft_df.values[:,4]    # 2971

    # 2-means labels
    mfcc_2_means = mfcc_df.values[:,5]
    stft_2_means = stft_df.values[:,5]

    # 6-means labels
    # Best cluster for MFCC is labeled 3
    mfcc_6_means = [(1 if x==3 else 0) for x in mfcc_df.iloc[:,3].values]
    # Possible best cluster for STFT is labeled 4
    stft_6_means_a = [(1 if x==4 else 0) for x in stft_df.iloc[:,3].values]
    # Possible best cluster for STFT is labeled 1
    stft_6_means_b = [(1 if x==1 else 0) for x in stft_df.iloc[:,3].values]


    # Run clusterig measures on MFCC

    # Rand score
    mfcc_2_score = cluster_rand_score(mfcc_ground_labels, mfcc_2_means)
    mfcc_6_score = cluster_rand_score(mfcc_ground_labels, mfcc_6_means)
    
    print(mfcc_2_score, mfcc_6_score)



