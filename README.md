# text mining in python

The code in this repository is meant to work on a cluster environment, together with [ToMaR](https://github.com/openpreserve/ToMaR).

This is currently work in progress (some scripts are not converted yet), thus it might not work in your environment at all.

## Installation 'entities':

Install nltk:

    pip install nltk
    
TODO: Configure the nltk_data directory.
    
Install the (german?) tokenizer:

    python (or: /opt/anaconda3/bin/python)
    >>> import nltk
    >>> nltk.download()
    >>> Downloader> d
    >>> Identifier> punkt
    
Edit some parameters:

In `start.sh`:

    export NLTK_DATA='/path/to/nltk_data'
    
also add the correct path to the input file and the `--hadoop-streaming-jar`.

In `mr_ner.py`:

    java_path = "/path/to/java_8_JRE/bin/java"
    model_ger = "/path/to/ner/model"
    stanford_jar = "/path/to/stanford-ner.jar"
