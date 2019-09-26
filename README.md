# MaSC Music Visualization

## Scripts Flow

### Data Organization

- Raw Music files on CDS-Carlos server
  - We need to decide on folders to use for analysis and set a definite folder structure

- `clip_extraction.py`

Extracts clips from the CDS-Carlos server to a local machine on which to do the computational analysis. Can be given parameters for length of the clips, number of clips, and position of the clips to extract. Saves the files in wav format in the original folder structure.

- `create_ids.py`

Within the local machine, remove duplicate songs, merges artists together, and in general organizes the collection. Can result in a new local folder structure. Outputs a csv file `song_ids.csv` where each clip is assigned a **Unique-ID** that will be used for the rest of the analysis, the file path to access it, and the metadata that can be extracted from it (Collection, Artist, Album, Genre, Year, Recording Method, Annotations, etc.)
  
- `corpus_statistics.py`

Computes statistics from the `song_ids.csv` file, such as number of Artists and Songs in each collection that can be presented as a table in the paper. Outputs a csv file `corpus_statistics.csv`.

### Computational Analysis

Each of the steps below constitutes an independent module, so that experiments can be done with any combination of parameters for each module. Eg. we can change the dimensionality reduction method in step _ and the sampling rate in step 1 and obtain a different visualization result.

1. `preprocessing.py`

Defines parameters to use for the computational analysis such as sampling rate and window size. Saves them in JSON format in a folder \preprocessing_parameters as `parameters_x.json` where *x* is the *x*th option.
