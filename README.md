# Da-TACOS

We present Da-TACOS: a dataset for cover song identification and understanding. It contains two subsets, namely benchmark subset and cover analysis subset, with pre-extracted features and metadata for 15,000 and 10,000 songs, respectively. The annotations included in the metadata are obtained with the API of [SecondHandSongs](https://secondhandsongs.com).

For organizing the data, we use the structure of SecondHandSongs where each song is called a 'performance', and each clique (cover group) is called a 'work'. Based on this, the file names of the songs are their unique performance IDs, and their labels with respect to their cliques are their work IDs.

Metadata for each song includes performance title, performance artist, work title, work artist, release year, SecondHandSongs.com performance ID, SecondHandSongs.com work ID, and whether the song is instrumental or not. In addition, we matched the original metadata with MusicBrainz to obtain MusicBrainz ID (MBID), song length and genre/style tags. We would like to note that MusicBrainz related information is not available for all the songs in Da-TACOS.

The pre-extracted features and the metadata can be found at [Link].

## Structure

### Metadata

We provide two metadata files that contain information about the benchmark subset and the cover analysis subset. Both metadata files are stored as python dictionaries in `.json` format, and have the same hierarchical structure. 

An example to load the metadata files in python:

```python
import json

with open('./metadata/da-tacos_benchmark_subset_metadata.json') as f:
	benchmark_metadata = json.load(f)
```

The python dictionary obtained with the code above will have the respective WIDs as keys. Each key will provide the song dictionaries that contain the metadata regarding the songs that belong to their WID. An example can be seen below:

```python
"W_163992": {
		"P_547131": {
			"work_title": "Trade Winds, Trade Winds",
			"work_artist": "Aki Aleong",
			"perf_title": "Trade Winds, Trade Winds",
			"perf_artist": "Aki Aleong",
			"release_year": "1961",
			"work_id": "W_163992",
			"perf_id": "P_547131",
			"instrumental": "No",
			"perf_artist_mbid": "9bfa011f-8331-4c9a-b49b-d05bc7916605",
			"mb_performances": {
				"4ce274b3-0979-4b39-b8a3-5ae1de388c4a": {
					"length": "175000"
				},
				"7c10ba3b-6f1d-41ab-8b20-14b2567d384a": {
					"length": "177653"
				}
			}
		},
		"P_547140": {
			"work_title": "Trade Winds, Trade Winds",
			"work_artist": "Aki Aleong",
			"perf_title": "Trade Winds, Trade Winds",
			"perf_artist": "Dodie Stevens",
			"release_year": "1961",
			"work_id": "W_163992",
			"perf_id": "P_547140",
			"instrumental": "No"
		}
	}
```


### Pre-extracted features

The list of features included in Da-TACOS can be seen in [Figure 1].

To facilitate the use of the dataset, we provide two options regarding the file structure.

1- In `da-tacos_benchmark_subset_single_files` and `da-tacos_coveranalysis_subset_single_files` files, we organize the data based on their respective cliques (cover groups), and one file contains all the features for that particular song. 

```python
{
	"chroma_cens": numpy.ndarray,
	"crema": numpy.ndarray,
	"hpcp": numpy.ndarray,
	"key_extractor": {
		"key": numpy.str_,
		"scale": numpy.str,_
		"strength": numpy.float64
	},
	"madmom_features": {
		"novfn": numpy.ndarray, 
		"onsets": numpy.ndarray,
		"snovfn": numpy.ndarray,
		"tempos": numpy.ndarray
	}
	"mfcc_htk": numpy.ndarray,
	"tags": list of (numpy.str,_numpy.str)
	"label": numpy.str_,
	"track_id": numpy.str_
}


```

2- In `da-tacos_benchmark_subset_FEATURE` and `da-tacos_coveranalysis_subset_FEATURE` folders, the data is organized based on their cliques as well, but each of these folders contain only one feature per song. For instance, if you want to test your system that uses HPCP features, you can download `da-tacos_benchmark_subset_hpcp` to access the pre-computed HPCP features. An example for the contents in those files can be seen below:

```python
{
	"hpcp": numpy.ndarray,
	"label": numpy.str_,
	"track_id": numpy.str_
}


```

## Using the dataset

### Downloading the data

The dataset is stored in Zenodo and can be downloaded in this [webpage]. We also provide a python script that automatically downloads the folder you specify. Basic usage of this script can be seen below:

### Loading the data in python

All files excluding the metadata are stored in `.h5` format. You must have `deepdish` library for Python to load the files. An example of how to load the data is shown below:

```python
import deepdish as dd

file_path = './da-tacos_coveranalysis_subset_single_files/W_22/P_22.h5'
P_22_data = dd.io.load(file_path)
```
