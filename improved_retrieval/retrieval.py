from nltk.stem import SnowballStemmer
import math
import csv
from collections import defaultdict

def stemmerFunc(wordList):
    stemmer = SnowballStemmer("english")
    returnList = []
    for word in wordList:
        returnList.append(stemmer.stem(word))
    return returnList

def queryVector(query, inverted_index, idf):
    query_tf = {term: query.count(term) for term in query}
    query_vector = [] # This is the TF-IDF of each term in the query
    for term in query:
        if term in inverted_index:
            query_vector.append(query_tf[term] * idf[term])
        else:
            query_vector.append(0)
    return query_vector


def documentVectors(inverted_index, idf, query_terms):
    docVector = defaultdict(lambda: [0.0] * len(query_terms))
    termIndex = {term: i for i, term in enumerate(query_terms)}

    for term in query_terms:
        if term in inverted_index:
            postings = inverted_index[term]
            for doc_id, tf in postings:
                tf_idf = int(tf) * idf[term]
                index = termIndex[term]
                docVector[doc_id][index] = tf_idf
    return docVector

def cosine_similarity(queryVector, docVector):
    cosineVector = []
    for index, value in enumerate(docVector):
        dot = sum(queryVector[i] * docVector[value][i] for i in range(len(queryVector)))
        magQ = math.sqrt(sum(queryVector[i] ** 2 for i in range(len(queryVector))))
        magD = math.sqrt(sum(docVector[value][i] ** 2 for i in range(len(docVector[value]))))
        if magQ == 0 or magD == 0:
            cosine = 0
        else:
            cosine = dot / (magQ * magD)
        cosineVector.append([value, cosine])
    cosineVector.sort(key=lambda x: x[1], reverse=True)
    return cosineVector

def main():
    inverted_index = {}
    with open('inverted_index_single_line.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            inverted_index[row[0]] = [doc_freq.split(":") for doc_freq in row[1:]]

    query = input("Enter query: ")
    query = query.lower()
    query = query.split(" ")
    query = stemmerFunc(query)

    df = { # How many documents each term appears in
        term: len(postings) for term, postings in inverted_index.items()
    }
    N = 500 # Number of documents in tokenized_project2_project2_crawl
    idf = {term: math.log(N / df_val) for term, df_val in df.items()}

    query_vector = queryVector(query, inverted_index, idf)
    docVectors = documentVectors(inverted_index, idf, query) # Returns document vectors in the same order as the original search query
    cosineVector = cosine_similarity(query_vector, docVectors)

    numToPrint = input("Up to how many pages do you want to print, type 0 for all: ")
    if numToPrint == "0" or int(numToPrint) > len(cosineVector):
        numToPrint = len(cosineVector)
    else:
        numToPrint = int(numToPrint)

    for index, doc in enumerate(cosineVector[:numToPrint]):
        print(f'Document Name: {doc[0].split(".")[0]}, Cosine Similarity: {doc[1]}, Rank: {index + 1}')
    

if __name__ == "__main__":
    main()