# vector-db-comparison
Basic code to compare different vector databases regarding semantic search performance and retrieval quality. 

## Background
The goal is to compare different vector databases regarding semantic search capabilities on a real-world dataset. This project included

FAISS: https://github.com/facebookresearch/faissqdra

Qdrant: https://qdrant.tech/

Weaviate: https://weaviate.io/

ELSER (v2): https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html

## Setup
To start, please download this Kaggle dataset locally:

https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset

Then install all necessary dependencies

    pip3 install -rm requirements.txt

Now first cleanup the data using

    python3 cleanup-csv.py

and then continue with the code in the respective subdirectory. Go through the files beforehand and set the necessary credentials if needed. The code is pretty repetitive by intention, I started with FAISS so you should probably do so too to see the pattern that is basically the same for all products (with slight variations).