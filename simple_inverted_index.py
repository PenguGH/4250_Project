import os
import csv
from collections import defaultdict

def build_inverted_index_with_tf(folder_path):
    inverted_index = defaultdict(lambda: defaultdict(int))  # term = {doc: frequency}

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                tokens = f.read().split()
                for token in tokens:
                    inverted_index[token][filename] += 1

    return dict(inverted_index)

def export_index_to_csv_single_line(index, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["term", "postings"])  # header

        for term, doc_dict in index.items():
            postings = [f"{doc}:{freq}" for doc, freq in sorted(doc_dict.items())]
            writer.writerow([term] + postings)


if __name__ == "__main__":
    folder_path = "stemmed_project2_crawl_en"  
    output_csv = "inverted_index_single_line.csv"

    index = build_inverted_index_with_tf(folder_path)
    export_index_to_csv_single_line(index, output_csv)

    print(f"Single-line inverted index exported to: {output_csv}")

