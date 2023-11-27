import csv
import re
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer

# Script to find out the longest song in the collection of songs in the CSV with regards to token length
csv_file = 'spotify_millsongdata_cleaned.csv'

lyrics_column = 'text'

max_length = 0
max_word_count = 0
row_with_longest_text = None
all_word_count = 0

# Define a regular expression to split text into words.
word_pattern = re.compile(r'\w+')

# Open the CSV file and iterate through the rows.
with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        # Access the text in the specified column.
        text = row[lyrics_column]
        
        # Calculate the length of the text and word count in the column.
        text_length = len(text)
        word_count = len(word_pattern.findall(text))

        all_word_count = all_word_count + word_count
        
        # Check if this row has the longest text.
        if text_length > max_length:
            max_length = text_length
            max_word_count = word_count
            row_with_longest_text = row

# Print the row with the longest text, its length, and word count.
if row_with_longest_text is not None:
    print("Row with the longest text:")
    print(row_with_longest_text)
    #print("Length of the text:", max_length)
    print("Word count:", max_word_count)
else:
    print("No data found in the specified column.")

print("All word count:", all_word_count)    

longest_lyrics = row_with_longest_text[lyrics_column]

model_name = 'all-mpnet-base-v2'
model = SentenceTransformer(model_name)

# that's the sentence transformer
print("Max sequence length of model: {}".format(model.max_seq_length))
# that's the underlying transformer
print("Transformer max embeddings: {}".format(model[0].auto_model.config.max_position_embeddings))

tokens = model.tokenizer.tokenize(longest_lyrics)
print("Number of tokens in the text: {}".format(len(tokens)))