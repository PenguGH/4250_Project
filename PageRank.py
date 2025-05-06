#Part 4: PageRank
import numpy as np
import pandas as pd
import ast

#reads links from report files and builds a graph
def load_links_from_reports(report_files):
    links = {}
    all_pages = set()

    for file in report_files:
        print(f"Reading file: {file}")
        try:
            #reads CSV w/ quoted fields and line skipping
            data = pd.read_csv(file, quotechar='"', on_bad_lines='skip')
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        for _, row in data.iterrows():
            source = row.get('URL', '')
            try:
                #reads  list of outlinks stored as string in CSV
                outlinks_raw = row.get('Outlinks', '[]')
                outlinks = ast.literal_eval(outlinks_raw)
                if not isinstance(outlinks, list):
                    outlinks = []
            except:
                outlinks = []

            #shows what's being parsed
            print(f"SOURCE: {source}")
            print(f"OUTLINKS: {outlinks}")

            links[source] = outlinks
            all_pages.add(source)
            for link in outlinks:
                all_pages.add(link)

    return links, list(all_pages)

#calculates PageRank using power iteration
def calculate_pagerank(links, pages, damping=0.85, max_steps=100, threshold=1e-6):
    total_pages = len(pages)

    if total_pages == 0:
        print("Error: No pages found. Check your input files or parsing logic.")
        return {}

    page_to_index = {page: i for i, page in enumerate(pages)}
    index_to_page = {i: page for i, page in enumerate(pages)}

    #creates a matrix to store link probabilities
    matrix = np.zeros((total_pages, total_pages))

    for source, outlinks in links.items():
        if source not in page_to_index:
            continue

        source_index = page_to_index[source]

        if len(outlinks) == 0:
            #dangling node/distribute evenly
            matrix[:, source_index] = 1.0 / total_pages
        else:
            prob = 1.0 / len(outlinks)
            for target in outlinks:
                if target in page_to_index:
                    target_index = page_to_index[target]
                    matrix[target_index][source_index] = prob

    #start w/ equal ranks
    ranks = np.ones(total_pages) / total_pages

    for step in range(max_steps):
        new_ranks = (1 - damping) / total_pages + damping * matrix.dot(ranks)
        change = np.linalg.norm(new_ranks - ranks, 1)
        if change < threshold:
            break
        ranks = new_ranks

    #converts result to a dictionary
    pagerank_scores = {}
    for i in range(total_pages):
        pagerank_scores[index_to_page[i]] = ranks[i]

    return pagerank_scores

#sort and show top 100 pages
def get_top_100_pages(pagerank_scores):
    sorted_pages = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_pages[:100]

#main program
def main():
    #lists report files
    report_files = [
        "report_project2_crawl_en.csv"
    ]

    print("Reading crawl data...")
    link_graph, all_pages = load_links_from_reports(report_files)

    if not all_pages:
        print("No pages were loaded. Exiting.")
        return

    print("Calculating PageRank...")
    pageranks = calculate_pagerank(link_graph, all_pages)

    if not pageranks:
        print("PageRank calculation failed.")
        return

    print("Top 100 Pages by PageRank:")
    top_pages = get_top_100_pages(pageranks)
    for i, (url, score) in enumerate(top_pages, 1):
        print(f"{i:3d}. {url} — {score:.6f}")

if __name__ == "__main__":
    main()