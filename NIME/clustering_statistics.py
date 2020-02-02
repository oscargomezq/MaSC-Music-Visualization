import os
import numpy as np
import pandas as pd
from sklearn import metrics


# Calculate cluster purity
def cluster_purity (ground_labels, assigned_labels):
	# https://stackoverflow.com/a/51672699
    # compute contingency matrix (also called confusion matrix)
    contingency_matrix = metrics.cluster.contingency_matrix(ground_labels, assigned_labels)
    print(contingency_matrix)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix) 



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
    mfcc_ground_labels = mfcc_df.values[:,4]    # 2792
    stft_ground_labels = stft_df.values[:,4]    # 2791

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

    # Cluster purity
    mfcc_2_purity = cluster_purity(mfcc_ground_labels, mfcc_2_means)
    mfcc_6_purity = cluster_purity(mfcc_ground_labels, mfcc_6_means)
    print("Purity scores:", mfcc_2_purity, mfcc_6_purity)
    # Rand score
    mfcc_2_rand = metrics.adjusted_rand_score(mfcc_ground_labels, mfcc_2_means)
    mfcc_6_rand = metrics.adjusted_rand_score(mfcc_ground_labels, mfcc_6_means)
    print("Rand scores:", mfcc_2_rand, mfcc_6_rand)
    # Cluster entropy, completeness, v_score
    mfcc_2_ecv = metrics.homogeneity_completeness_v_measure(mfcc_ground_labels, mfcc_2_means)
    mfcc_6_ecv = metrics.homogeneity_completeness_v_measure(mfcc_ground_labels, mfcc_6_means)
    print("ECV scores:", mfcc_2_ecv, mfcc_6_ecv)


    # Run clusterig measures on STFT

    # Cluster purity
    stft_2_purity = cluster_purity(stft_ground_labels, stft_2_means)
    stft_6_purity_a = cluster_purity(stft_ground_labels, stft_6_means_a)
    stft_6_purity_b = cluster_purity(stft_ground_labels, stft_6_means_b)
    print("Purity scores:", stft_2_purity, stft_6_purity_a, stft_6_purity_b)
    # Rand score
    stft_2_rand = metrics.adjusted_rand_score(stft_ground_labels, stft_2_means)
    stft_6_rand_a = metrics.adjusted_rand_score(stft_ground_labels, stft_6_means_a)
    stft_6_rand_b = metrics.adjusted_rand_score(stft_ground_labels, stft_6_means_b)
    print("Rand scores:", stft_2_rand, stft_6_rand_a, stft_6_rand_b)
    # Cluster entropy, completeness, v_score
    stft_2_ecv = metrics.homogeneity_completeness_v_measure(stft_ground_labels, stft_2_means)
    stft_6_ecv_a = metrics.homogeneity_completeness_v_measure(stft_ground_labels, stft_6_means_a)
    stft_6_ecv_b = metrics.homogeneity_completeness_v_measure(stft_ground_labels, stft_6_means_b)
    print("ECV scores:", stft_2_ecv, stft_6_ecv_a, stft_6_ecv_b)

    
    



