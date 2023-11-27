import pandas as pd
from elasticsearch import Elasticsearch, helpers

import configparser

# This script loads the songs data and imports it into an ElasticSearch index for later processing
config = configparser.ConfigParser()
config.read('config.ini')

client = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

client.info()

# Define your Elasticsearch index name
index_name = 'spotify-data'

# Read the CSV file
df = pd.read_csv('spotify_millsongdata_cleaned.csv')

# Loop through the CSV rows and index them in Elasticsearch
for _, row in df.iterrows():
    document = row.to_dict()
    client.index(index=index_name, body=document)

# Refresh the index to make the data immediately available for searching
client.indices.refresh(index=index_name)