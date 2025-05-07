import numpy as np
import pandas as pd
import ast
import csv

# Load link graph from CSV with columns URL and Outlinks
def load_links_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    links = {}
    pages = set()
    for _, row in df.iterrows():
        src = row['URL']
        raw = row['Outlinks']
        try:
            outs = [u.strip() for u in ast.literal_eval(raw)]
        except Exception:
            outs = []
        links[src] = outs
        pages.add(src)
        for tgt in outs:
            pages.add(tgt)
    return links, list(pages)

# Calculate PageRank via power iteration
def calculate_pagerank(links, pages, damping=0.85, max_iter=100, tol=1e-6):
    N = len(pages)
    index = {page: i for i, page in enumerate(pages)}
    M = np.zeros((N, N))
    # Build transition matrix
    for src, outs in links.items():
        j = index[src]
        if outs:
            w = 1.0 / len(outs)
            for tgt in outs:
                if tgt in index:
                    i = index[tgt]
                    M[i, j] = w
        else:
            M[:, j] = 1.0 / N
    # Initialize rank vector
    pr = np.ones(N) / N
    for _ in range(max_iter):
        new_pr = (1 - damping) / N + damping * M.dot(pr)
        if np.linalg.norm(new_pr - pr, 1) < tol:
            break
        pr = new_pr
    return {pages[i]: pr[i] for i in range(N)}

# Get top-N pages by rank
def get_top_n(ranks, n=100):
    return sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:n]

if __name__ == '__main__':
    csv_file = 'report_project2.1_crawl_en.csv'
    links, pages = load_links_from_csv(csv_file)
    ranks = calculate_pagerank(links, pages)
    top100 = get_top_n(ranks, 100)

    # write all PageRank scores sorted by rank
    all_output = 'pagerank_all_pages.csv'
    sorted_all = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
    with open(all_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'URL', 'PageRank'])
        for i, (url, score) in enumerate(sorted_all, 1):
            writer.writerow([i, url, f"{score:.6f}"])
    print(f"All PageRank scores written to {all_output}")

