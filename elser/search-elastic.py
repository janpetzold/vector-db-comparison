import pandas as pd
import time
from elasticsearch import Elasticsearch, helpers

import configparser

# This script searches for a user query via ELSER semantic search
config = configparser.ConfigParser()
config.read('config.ini')

client = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)


query = {
  "track_total_hits": False,
  "query": {
    "text_expansion": {
         "text_embedding": {
            "model_id":".elser_model_2_linux-x86_64",
            "model_text":"What song mentions most of the cities in Europe"
         }
      }
  },
  "size": 3
}

t = time.time()
res = client.search(index='vector-index', body=query)
print('Query finished in: {}'.format(time.time()-t))

for hit in res['hits']['hits']:
    print("Song is " + hit["_source"]["song"] + " from artist " + hit["_source"]["artist"] + " with a score of " + str(hit["_score"]))
