from nltk.stem import SnowballStemmer
import csv

def stemmerFunc(wordList):
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(word) for word in wordList]

def main():
    inverted_index = {}

    # Load inverted index
    with open('inverted_index_single_line.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            term = row[0]
            postings = [doc_freq.split(":")[0] for doc_freq in row[1:]]
            inverted_index[term] = postings
    
    # CLI: get query from user
    userQuery = input("Please enter your query: ").lower().split()
    userQuery = stemmerFunc(userQuery)

    # Collect sets of documents for each query term
    result_sets = []
    for term in userQuery:
        if term in inverted_index:
            result_sets.append(set(inverted_index[term]))
        else:
            result_sets.append(set()) # no results found for the query term
    
    if not result_sets:
        print("No relevant results found.")
        return
    
    # (Boolean AND) to interesect the result sets
    relevant_docs = set.intersection(*result_sets)

    if relevant_docs:
        print("Relevant results are:", ", ".join(sorted(relevant_docs)))
    else:
        print("No relevant results found.")

if __name__ == "__main__":
    main()
