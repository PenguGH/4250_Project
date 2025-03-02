
# install: pip install nltk
import os
import nltk
from nltk.stem import SnowballStemmer

# Ensure required NLTK downloads
nltk.download('punkt')

# Define source folders
source_folders = {
    "de": r"C:/Users/wangr/OneDrive/Desktop/Web Reccom/Project1/4250_Project_1/tokenized_crawl_de",
    "en": r"C:/Users/wangr/OneDrive/Desktop/Web Reccom/Project1/4250_Project_1/tokenized_crawl_en",
    "fr": r"C:/Users/wangr/OneDrive/Desktop/Web Reccom/Project1/4250_Project_1/tokenized_crawl_fr"
}

output_folders = {
    "de": r"C:/Users/wangr/OneDrive/Desktop/Web Reccom/Project1/4250_Project_1/stemmed_crawl_de",
    "en": r"C:/Users/wangr/OneDrive/Desktop/Web Reccom/Project1/4250_Project_1/stemmed_crawl_en",
    "fr": r"C:/Users/wangr/OneDrive/Desktop/Web Reccom/Project1/4250_Project_1/stemmed_crawl_fr"
}

# Initialize stemmers
stemmers = {
    "de": SnowballStemmer("german"),
    "en": SnowballStemmer("english"),
    "fr": SnowballStemmer("french")
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

    for filename in os.listdir(source_folder):  # Loop through each text file
        if filename.endswith(".txt"):  # Process only .txt files
            input_file = os.path.join(source_folder, filename)
            output_file = os.path.join(output_folders[lang], filename)

            print(f"Processing {filename}...")
            process_file(input_file, output_file, lang)

    print(f"Finished processing {lang}! Stemmed files saved in {output_folders[lang]}\n")