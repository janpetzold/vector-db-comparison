from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import pandas as pd
import csv
import pickle
from qdrant_client.models import PointStruct
import numpy as np

# Before executing start qdrant via
# docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

encoder = SentenceTransformer('all-mpnet-base-v2') 

qdrant = QdrantClient("localhost", port=6333)

qdrant.recreate_collection(
	collection_name="allsongs",
	vectors_config=models.VectorParams(
		size=encoder.get_sentence_embedding_dimension(),
		distance=models.Distance.COSINE,
        on_disk=True
	)
)

csv_file = "spotify_millsongdata_cleaned.csv"
lyrics_file = "lyrics_embeddings_all-mpnet-base-v2.pkl"

print("Loading embeddings from disk")
with open(lyrics_file, "rb") as f:
    lyrics_embeddings = pickle.load(f)

all_records = []

with open(csv_file, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        if i > 0:
            #print("line[{}] = {}".format(i, line[0]))
            artist = line[0]
            song = line [1]
            #print("Line {} has artist {} with song {}".format(i, artist, song))
            #print("Corresponding vector is")
            #print(lyrics_embeddings[i - 1])
            lyrics = lyrics_embeddings[i - 1]

            idx = i - 1

            current_payload = {}
            current_payload['artist'] = artist
            current_payload['song'] = song

            record = models.Record(
                id=idx,
                vector=lyrics_embeddings[i - 1].tolist(),
                payload=current_payload
            )
            all_records.append(record)

qdrant.upload_records(
	collection_name="allsongs",
	records=all_records,
    batch_size=256,
    max_retries=3
)