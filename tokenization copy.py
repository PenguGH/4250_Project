# Going to read through the files found in repositories for crawl, will tokenize each file and write the tokenized file to to a folder called tokenized_crawl_whatever
# language is there.


# Read through the folders repository_crawl_en, repository_crawl_de, repository_crawl_fr
# For each file in the folder, tokenize the file and write the tokenized file to a folder called tokenized_crawl_language
# The tokenized files will be a txt file of everything in the html file that isn't code
from bs4 import BeautifulSoup
import os
import re

def word_tokenize(text):
    cleantext = BeautifulSoup(text, "lxml").text
    cleantext = re.sub(r'\W+', ' ', cleantext)
    return cleantext

# Read through folders
for folder in ["repository_project2_crawl_en"]:
    # Read through files in folder
    folderName = f'tokenized_project2_{folder.split("_")[1]}_{folder.split("_")[2]}'
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    for file in os.listdir(folder):
        # Tokenize file
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            text = f.read()
            tokenized_text = word_tokenize(text)
            # Write tokenized file to folder
            fileName = file.split(".")[0]
            with open(os.path.join(folderName, fileName + ".txt"), "w", encoding="utf-8") as f:
                f.write(tokenized_text)
