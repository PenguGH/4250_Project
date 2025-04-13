
# install: pip install nltk
import os
import nltk
from nltk.stem import SnowballStemmer

# Ensure required NLTK downloads
nltk.download('punkt')

# Define source folders
source_folders = {
    "en": r"tokenized_project2_project2_crawl"
}   

output_folders = {
    "en": r"stemmed_project2_crawl_en",
}

# Initialize stemmers
stemmers = {
    "en": SnowballStemmer("english")
}

def process_file(input_file, output_file, language):
    """Reads a tokenized text file, applies stemming, and saves the output."""
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.readlines()  # Read all lines

    stemmed_documents = []
    for line in content:
        tokens = line.strip().split()  # Assuming space-separated tokens
        stemmed_tokens = [stemmers[language].stem(word) for word in tokens]
        stemmed_documents.append(" ".join(stemmed_tokens))  # Reconstruct text

    # Save the processed text into the corresponding output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(stemmed_documents))

# Process all files inside each language folder
for lang, source_folder in source_folders.items():
    print(f"Processing all files in {source_folder}...")

    os.makedirs(output_folders[lang], exist_ok=True)

    for filename in os.listdir(source_folder):  # Loop through each text file
        if filename.endswith(".txt"):  # Process only .txt files
            input_file = os.path.join(source_folder, filename)
            output_file = os.path.join(output_folders[lang], filename)

            print(f"Processing {filename}...")
            process_file(input_file, output_file, lang)

    print(f"Finished processing {lang}! Stemmed files saved in {output_folders[lang]}\n")