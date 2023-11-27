import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import time
import csv

# Read CSV as reference
songs = {}
with open("spotify_millsongdata_cleaned.csv", mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for line_number, row in enumerate(csv_reader, 1):  
        parent_id = line_number
        
        # Add the parent ID to the row as a new key-value pair
        row['id'] = parent_id
        
        # Add the row to the data dictionary with the parent ID as the key
        songs[parent_id] = row

# Load a pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')
index = faiss.read_index('lyrics-ivf')

def search(query):
    print("Searching for query " + query)
    t = time.time()
    query_vector = model.encode([query])
    num_results = 3
    distances, top_results = index.search(query_vector, num_results)
    print('Query finished in: {}'.format(time.time()-t))

    element_list = top_results[0].tolist()

    # Create an empty list to store the results
    result_list = []

    distance_iterator = 0
    # Iterate through the indices in the 'first_element' list
    for _id in element_list:
        score = str(round(100 - abs(distances[0][distance_iterator]), 2))
        distance_iterator = distance_iterator + 1
        print("Song {} (ID {}) from artist {} has score of {}%".format(songs[_id+1]['song'], _id+1, songs[_id+1]['artist'], score))

search("There was a dance track containing a lot of la la la and a boy and a girl that should stay together forever and ever. It seems that she just can't stop thinking about him.")