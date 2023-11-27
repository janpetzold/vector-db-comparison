import re
import csv

# Replace 'input_file.csv' with your CSV file name and 'output_file.csv' with the desired output file name
input_file = 'spotify_millsongdata.csv'
output_file = 'spotify_millsongdata_cleaned.csv'

def clean_and_merge_text(text):
    # Replace line breaks with spaces, strip leading/trailing spaces, remove double-quote characters, and replace consecutive whitespaces
    return re.sub(r'\s+', ' ', text.strip().replace('"', ''))

with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
    csv_reader = csv.reader(input_csv)
    csv_writer = csv.writer(output_csv)

    # Read and write the header
    header = next(csv_reader)
    csv_writer.writerow(header)

    for row in csv_reader:
        # Clean and merge the "text" column
        row[3] = clean_and_merge_text(row[3])  # Assuming "text" is in the 4th column (0-based index)
        csv_writer.writerow(row)