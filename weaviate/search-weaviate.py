import weaviate
import json
import time
from sentence_transformers import SentenceTransformer

auth_config = weaviate.AuthApiKey(api_key="YOUR-API-KEY")

client = weaviate.Client(
  url="YOUR-WEAVIATE-URL",
  auth_client_secret=auth_config
)

model = SentenceTransformer('all-mpnet-base-v2')
query = "Will winter follow directly after summer?"
query_vector = model.encode([query])

t = time.time()
response = (
    client.query
      .get("songs", ["artist", "song"])
      .with_near_vector({
          "vector": query_vector
      })
      .with_additional("distance")
      .with_limit(3)
      .do()
)
print('Query finished in: {}'.format(time.time()-t))
print(json.dumps(response, indent=3))