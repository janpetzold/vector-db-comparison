import numpy as np
import torch
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import time
import re
import pickle
import math

# This script loads & indexes the songs to an Inverted File index
data = pd.read_csv('spotify_millsongdata_cleaned.csv')

# Load a pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')

# Create vectors
lyrics = data["text"].tolist()
t = time.time()
print("Encoding the embeddings")
lyrics_embeddings = model.encode(lyrics)
print('Embedding finished in: {}'.format(time.time()-t))

# Save model to disk
print("Saving multi-qa embeddings to disk")#
with open("lyrics_embeddings_small_all-mpnet-base-v2.pkl", "wb") as f:
    pickle.dump(lyrics_embeddings, f)

# Load model from disk
print("Loading embeddings from disk")
with open("lyrics_embeddings_all-mpnet-base-v2.pkl", "rb") as f:
    lyrics_embeddings = pickle.load(f)

# Create IVF index
nlist = 32  # number of clusters
quantiser = faiss.IndexFlatL2(lyrics_embeddings.shape[1])  
index = faiss.IndexIVFFlat(quantiser, lyrics_embeddings.shape[1], nlist,faiss.METRIC_L2)
index.train(lyrics_embeddings)
index.add(lyrics_embeddings)
faiss.write_index(index, 'lyrics-ivf')