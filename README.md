# MaSC Music Visualization

## Data Organization

Raw Music files on CDS-Carlos server.
  - We need to decide on folders to use for analysis and set a definite folder structure.

`clip_extraction.py`

Extracts clips from the CDS-Carlos server to a local machine on which to do the computational analysis. Can be given parameters for length of the clips, number of clips, and position of the clips to extract. Saves the files in wav format in the original folder structure.

`create_ids.py`

Within the local machine, remove duplicate songs, merges artists together, and in general organizes the collection. Can result in a new local folder structure. Outputs a csv file `song_ids.csv` where each clip is assigned a **Unique-ID** that will be used for the rest of the analysis, the file path to access it, and the metadata that can be extracted from it (Collection, Artist, Album, Genre, Year, Recording Method, Annotations, etc.).
  
`corpus_statistics.py`

Computes statistics from the `song_ids.csv` file, such as number of Artists and Songs in each collection that can be presented as a table in the paper. Outputs a csv file `corpus_statistics.csv`.

## Computational Analysis

### Feature extraction and dimensionality reduction

Each of the scripts below constitutes an independent module, so that experiments can be done with any combination of parameters for each module. E.g. we can change the dimensionality reduction method in step 3 and the sampling rate in step 1 and obtain a different visualization result. The final 2D or 3D datasets that can be visualized are indentified by the combination of parameters for each step in its file name.

1. `preprocessing.py`

  - Defines parameters to use for the computational analysis such as sampling rate and window size. Saves them in JSON format in a folder *\preprocessing_parameters* as `parameters_preprocessing_x.json` where *x* is the *x*th option for parameters in step 1.

2. `feature_extraction.py`

  - Extract the musical features to be used for the analysis. Given parameters for features to use, and how many to extract. E.g. Extract 13 MFCC's per window, or extract the Spectrogram. Outputs a full-dimensionality dataset where each row corresponds to a clip that is identified by its **Unique-ID** and is followed by the extracted features. It is saved in csv format in a folder *\full_datasets* as `full_dataset_a_b.csv` where *a* is the *a*th option for parameters in step 1 and *b* is the *b*th option for parameters in step 2. The parameters for this step are stored as `parameters_feature_extraction_x.json` where *x* is the *x*th option for parameters in step 2.

3. `mid_dimension.py`

  - Reduces the dimensionality of a given working dataset. Given parameters for the method to use (PCA, Autoencoder and its architecture, etc.). Outputs a mid-dimensionality dataset in the same format as a full-dimensionality dataset but with less features per row. It is saved in csv format in a folder *\mid_datasets* as `mid_dataset_a_b_c.csv` following the convention described above where *c* is the *c*th option for parameters in step 3. The parameters for this step are stored as `parameters_mid_dimension_x.json` where *x* is the *x*th option for parameters in step 3.

4. `small_dimension.py`

  - Reduces the dimensionality of a given mid-dimensionality dataset. Given parameters for the method to use (PCA, tSNE, etc.). Outputs a small-dimensionality dataset in the same format as a working dataset but with 2 or 3 features per row. It is saved in csv format in a folder *\small_datasets* as `small_dataset_a_b_c_d.csv` following the convention described above where *d* is the *d*th option for parameters in step 4. The parameters for this step are stored as `parameters_small_dimension_x.json` where *x* is the *x*th option for parameters in step 4. The results of this step are 2D and 2D dimensionality files that can be visualized with the `2d_visualization.py` or `3d_visualization.py` scripts.

### Clustering and Visualization

Each of the scripts below constitutes an independent module, so that experiments can be done with any combination of parameters for each module. E.g. we can change the clustering method and the dataset to cluster on to obtain a different visualization result. The final HTML files are indentified by the combination of parameters for each step in its file name.

1. `clustering.py`

  - Performs clustering of a given dataset. Given parameters for the method to use (k-means, spectral, etc.) and the full, mid, or small dimensionality dataset to use. Outputs a label for each element identified by a **Unique-ID**. It is saved in csv format in a folder *\clustering_labels* as `cluster_labels_x_(dataset_id).csv` following the convention described above where *dataset_id* is the combination of parameters for the dataset and *x* is the *x*th option for parameters in the clustering step. The parameters for this step are stored as `parameters_clustering_x.json` where *x* is the *x*th option for parameters in the clustering step.

2. `2d_visualization.py` and `3d_visualization.py`

  - Creates an web visualization for a given 2D or 3D dataset and a set of clustering labels. Given parameters for the small-dimensionality dataset to use and clustering labels to use. Outputs an HTML file in a folder *\visualizations* as `nD_visualization_labels_x_(dataset_id)_data_a_b_c_d.csv` following the conventions described above where *n* is 2 or 3, *x_(dataset_id)* identifies the labels to use and *a_b_c_d* identifies the 2D or 3D dataset to use. 
