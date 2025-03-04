import os
import collections
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#function for computing word frequencies
def compute_word_frequencies(directory):
    word_counts = collections.Counter()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.read().split()
            word_counts.update(words)
    return word_counts

#function for plotting Zipf's Law (3A)
def plot_zipfs_law(word_counts, title):
    sorted_words = word_counts.most_common()
    ranks = list(range(1, len(sorted_words) + 1))
    frequencies = [count for _, count in sorted_words]
    
    plt.figure(figsize=(10, 5))
    plt.loglog(ranks, frequencies, marker="o", linestyle="none")
    plt.xlabel("Rank (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.title(f"Zipf's Law Plot - {title}")
    plt.grid(True)
    plt.show()

#function computing and plotting Heap's Law (3B)
def plot_heaps_law(word_counts, title):
    words_seen = set()
    vocab_growth = []
    collection_sizes = []
    total_words = 0
    
    for word, freq in word_counts.most_common():
        for _ in range(freq):
            words_seen.add(word)
            total_words += 1
            vocab_growth.append(len(words_seen))
            collection_sizes.append(total_words)
    
    plt.figure(figsize=(10, 5))
    plt.plot(collection_sizes, vocab_growth, label=title)
    plt.xlabel("Total Words in Collection")
    plt.ylabel("Unique Words (Vocabulary Size)")
    plt.title("Heap's Law: Vocabulary Growth vs Collection Size")
    plt.legend()
    plt.grid(True)
    plt.show()

#saves top 50 words to CSV (part of finla submission)
def save_top_words_to_csv(word_counts, filename):
    top_words = word_counts.most_common(50)
    df = pd.DataFrame(top_words, columns=["Word", "Frequency"])
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved top 50 words to {filename}")

#correct depository path for GitHub  
tokenized_paths = { 
    "crawl2": "tokenized_crawl_fr",
    "crawl3": "tokenized_crawl_de"
}

#processes each crawl
top_csv_files = {}
for crawl, path in tokenized_paths.items():
    word_counts = compute_word_frequencies(path)
    
    #plots Zipf's Law (3A)
    plot_zipfs_law(word_counts, crawl)
    
    #plots Heap's Law (3B)
    plot_heaps_law(word_counts, crawl)
    
    #saves top 50 words
    csv_filename = f"./Tokenization/Words{crawl[-1]}.csv"  #saves CSVs in Tokenization folder
    save_top_words_to_csv(word_counts, csv_filename)
    top_csv_files[crawl] = csv_filename