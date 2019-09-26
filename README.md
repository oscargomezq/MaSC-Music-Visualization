# MaSC Music Visualization

## Scripts Flow

### Data Organization

Raw Music files on CDS-Carlos server
  - We need to decide on folders to use for analysis and set a definite folder structure

`clip_extraction.py`

Extracts clips from the CDS-Carlos server to a local machine on which to do the computational analysis. Can be given parameters for length of the clips, number of clips, and position of the clips to extract. Saves the files in wav format in the original folder structure.

`create_ids.py`

Within the local machine, remove duplicate songs, merges artists together, and in general organizes the collection. Can result in a new local folder structure. Outputs a csv file `song_ids.csv` where each clip is assigned a **Unique-ID** that will be used for the rest of the analysis, the file path to access it, and the metadata that can be extracted from it (Collection, Artist, Album, Genre, Year, Recording Method, Annotations, etc.)
  
`corpus_statistics.py`

Computes statistics from the `song_ids.csv` file, such as number of Artists and Songs in each collection that can be presented as a table in the paper. Outputs a csv file `corpus_statistics.csv`.

### Computational Analysis

Each of the steps below constitutes an independent module, so that experiments can be done with any combination of parameters for each module. E.g. we can change the dimensionality reduction method in step _ and the sampling rate in step 1 and obtain a different visualization result. The final 2D or 3D datasets that can be visualized are indentified by the combination of parameters for each step in its file name.

1. `preprocessing.py`

- Defines parameters to use for the computational analysis such as sampling rate and window size. Saves them in JSON format in a folder \preprocessing_parameters as `parameters_a.json` where *x* is the *a*th option for parameters.

2. `feature_extraction.py`

- Extract the musical features to be used for the analysis. Given parameters for features to use, and how many to extract. E.g. Extract 13 MFCC's per window, or extract the Spectrogram. Outputs a working dataset where each row corresponds to a clip that is identified by its **Unique-ID** and is followed by the extracted features. It is saved in csv format in a folder \working_datasets as `dataset_a_b.csv` where *a* is the *a*th option for parameters in step 1 and *b* is the *b*th option for parameters in step 2.

3. `mid_dimension.py`

- Reduces the dimensionality of a given working dataset. Given parameters for the method to use (PCA, Autoencoder and its architecture, etc.). Outputs a mid-dimensionality dataset in the same format as a working dataset but with less features per row. It is saved in csv format in a folder \mid_datasets as `mid_dataset_a_b_c.csv` following the convention described above where *c* is the *c*th option for parameters in step 3.





