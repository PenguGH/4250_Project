from nltk.stem import SnowballStemmer
import os
import math
import csv
import sys


def safe_print(data):
    encoded = str(data).encode('ascii', errors='replace').decode('ascii')
    print(encoded)


def stemmerFunc(wordList):
    stemmer = SnowballStemmer("english")
    returnList = []
    for word in wordList:
        returnList.append(stemmer.stem(word))
    return returnList

def main():
    inverted_index = {}
    with open('inverted_index_single_line.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        counter = 10
        for row in reader:
            inverted_index[row[0]] = [doc_freq.split(":") for doc_freq in row[1:]]
            if counter >= 0:

                # safe_print(row[0])
                # # safe_print(row[1])
                # safe_print(inverted_index[row[0]])

                counter -= 1
    # Pretty output to file
    # For debugging
    # with open('inverted_index_output.txt', 'w', encoding='utf-8') as f:
    #     for term, postings in inverted_index.items():
    #         f.write(f"{term}: {postings}\n")

    # query = input("Enter query: ")
    query = "Los angeles dodgers"
    query = query.lower()
    query = query.split(" ")
    query = stemmerFunc(query)

    # # For debugging
    # print(query)

    df = { # How many documents each term appears in
        term: len(postings) for term, postings in inverted_index.items()
    }
    # safe_print(df)

    N = 500 # Number of documents in tokenized_project2_project2_crawl
    idf = {term: math.log(N / df_val) for term, df_val in df.items()}
    # safe_print(idf)

    query_tf = {term: query.count(term) for term in query}
    query_vector = []
    for term in query:
        # print(term, query_tf[term], idf[term])
        if term in inverted_index:
            query_vector.append(query_tf[term] * idf[term])
        else:
            query_vector.append(0)

    # safe_print(query_vector)
    # safe_print(query)

if __name__ == "__main__":
    main()