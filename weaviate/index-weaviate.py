import weaviate
import csv
import pickle
import uuid

auth_config = weaviate.AuthApiKey(api_key="YOUR-APIKEY")

client = weaviate.Client(
  url="YOUR-WEAVIATE-URL",
  auth_client_secret=auth_config
)

# Reset data
client.schema.delete_all()

class_obj = {
  "class": "songs",
  "vectorIndexType": "hnsw"
}

client.schema.create_class(class_obj)

print("Loading embeddings from disk")
lyrics_file = "lyrics_embeddings_all-mpnet-base-v2.pkl"
with open(lyrics_file, "rb") as f:
    lyrics_embeddings = pickle.load(f)

with open("spotify_millsongdata_cleaned.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")

    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:  # Initialize a batch process
        for i, line in enumerate(reader):
            if i > 0:
                #print("line[{}] = {}".format(i, line[0]))
                artist = line[0]
                song = line[1]
                lyrics = line[3]
                print("Line {} has artist {} with song {}".format(i, artist, song))

                properties = {
                    "artist": artist,
                    "song": song,
                    "lyrics": lyrics,
                }
                batch.add_data_object(
                    data_object=properties,
                    class_name="songs",
                    uuid=uuid.uuid4(),
                    vector=lyrics_embeddings[i - 1].tolist()
                )