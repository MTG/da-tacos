# Da-TACOS

We present Da-TACOS: a dataset for cover song identification and understanding. It contains two subsets, namely the benchmark subset and the cover analysis subset, with pre-extracted features and metadata for 15,000 and 10,000 songs, respectively. The annotations included in the metadata are obtained with the API of [SecondHandSongs.com](https://secondhandsongs.com).

For organizing the data, we use the structure of SecondHandSongs where each song is called a 'performance', and each clique (cover group) is called a 'work'. Based on this, the file names of the songs are their unique performance IDs (PID, e.g. `P_22`), and their labels with respect to their cliques are their work IDs (WID, e.g. `W_15`).

Metadata for each song includes performance title, performance artist, work title, work artist, release year, SecondHandSongs.com performance ID, SecondHandSongs.com work ID, and whether the song is instrumental or not. In addition, we matched the original metadata with MusicBrainz to obtain MusicBrainz ID (MBID), song length and genre/style tags. We would like to note that MusicBrainz related information is not available for all the songs in Da-TACOS.

For facilitating reproducibility in cover song identification (CSI) research, we propose two frameworks for feature extraction and benchmarking in our supplementary repository: [acoss](https://github.com/furkanyesiler/acoss). The feature extraction framework is designed to help CSI researchers to find the most commonly used features for CSI in a single address. The parameter values we used to extract the features in Da-TACOS are shared in the same repository. Moreover, the benchmarking framework includes our implementations of 7 state-of-the-art CSI systems. We provide the performance results of an initial benchmarking of those 7 systems on the benchmark subset of Da-TACOS. We encourage other CSI researchers to contribute to the open source frameworks with implementing their favorite feature extraction algorithms and their CSI systems to build up a knowledge base where CSI research can reach larger audiences.

The instructions for how to download and to use the dataset are shared below. Please contact us if you have any questions or requests.

## Structure

### Metadata

We provide two metadata files that contain information about the benchmark subset and the cover analysis subset. Both metadata files are stored as python dictionaries in `.json` format, and have the same hierarchical structure. 

An example to load the metadata files in python:

```python
import json

with open('./metadata/da-tacos_benchmark_subset_metadata.json') as f:
	benchmark_metadata = json.load(f)
```

The python dictionary obtained with the code above will have the respective WIDs as keys. Each key will provide the song dictionaries that contain the metadata regarding the songs that belong to their WIDs. An example can be seen below:

```python
"W_163992": { # work id
	"P_547131": { # performance id of the first song belonging to the clique 'W_163992'
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
	"P_547140": { # performance id of the second song belonging to the clique 'W_163992'
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

1- In `da-tacos_benchmark_subset_single_files` and `da-tacos_coveranalysis_subset_single_files` folders, we organize the data based on their respective cliques, and one file contains all the features for that particular song. 

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

### Requirements

* Python 3.6+
* Virtualenv: `pip install virtualenv`
* Create virtual environment and install requirements
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Downloading the data

The dataset is stored in Zenodo and can be downloaded in this [webpage]. We also provide a python script that automatically downloads the folder you specify. Basic usage of this script can be seen below:

```bash
python download_da-tacos.py -h
```
```
usage: download_da-tacos.py [-h]
                            [--dataset {benchmark,coveranalysis,da-tacos}]                                                                          
                            [--type {single_files,cens,crema,hpcp,key,madmom,mfcc,tags}]                                                            
                            [--outputdir OUTPUTDIR] 
                            [--unpack]
                            [--remove]

Download script for Da-TACOS 

optional arguments:                                                                                                       
  -h, --help            show this help message and exit                                                                   
  --dataset {benchmark,coveranalysis,da-tacos}                                                                      
                        which subsets to download. 'da-tacos' option downloads                                                                  
                        both subsets. metadata will be downloaded with all the                           
                        options. (default: benchmark)                                                                     
  --type {single_files,cens,crema,hpcp,key,madmom,mfcc,tags}                                                      
                        which folder to download. for the options other than                                      
                        'single_files', you can enter a list (e.g. ['cens',                                     
                        'crema']). for detailed explanation, please check                                                                       https://github.com/furkanyesiler/da-tacos (default:                                                                     single_files)                                     
                        (default: single_files)                                                                
  --outputdir OUTPUTDIR                                                               
                        directory to store the dataset (default: ./)                   
  --unpack              unpack the zip files (default: False)                        
  --remove              remove zip files after unpacking (default: False) 
```

### Loading the data in python

All files (except the metadata) are stored in `.h5` format. You must have `deepdish` library for python to load the files. An example of how to load the data is shown below:

```python
import deepdish as dd

file_path = './da-tacos_coveranalysis_subset_single_files/W_22/P_22.h5'
P_22_data = dd.io.load(file_path)
```

## Citing the dataset

Please cite the following publication when using the dataset:

> Furkan Yesiler, Chris Tralie, Albin Correya, Diego F. Silva, Philip Tovstogan, Emilia Gómez, and Xavier Serra. Da-TACOS: A Dataset for Cover Song Identification and Understanding. In 20th International Society for Music Information Retrieval Conference (ISMIR 2019), Delft, The Netherlands, 2019 (In print).

## License

* The code in this repository is licensed under [Apache 2.0](LICENSE) 
* The metadata and the pre-extracted features are licensed under a [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Acknowledgments

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 765068 (MIP-Frontiers).

This work has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 770376 (Trompa).

<img src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg" height="64" hspace="20">