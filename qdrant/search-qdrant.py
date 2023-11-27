from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import pandas as pd
from qdrant_client.models import PointStruct
import numpy as np
import time

encoder = SentenceTransformer('all-mpnet-base-v2') 
qdrant = QdrantClient("localhost", port=6333)            

t = time.time()
hits = qdrant.search(
	collection_name="songs",
	query_vector=encoder.encode("Which song is about the dreamy island of Java?").tolist(),
	limit=3
)
print('Query finished in: {}'.format(time.time()-t))

for hit in hits:
	print(hit.payload, "score:", hit.score)