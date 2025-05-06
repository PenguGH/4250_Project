# Part 4: PageRank with Outlinks Count only
import numpy as np
import pandas as pd
import random

# Reads links from report files and builds a graph
def load_links_from_reports(report_files):
    links = {}
    all_pages = set()

    for file in report_files:
        print(f"Reading file: {file}")
        try:
            data = pd.read_csv(file, quotechar='"', on_bad_lines='skip')
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        urls = data['URL'].tolist()
        outlink_counts = data['Outlinks Count'].fillna(0).astype(int).tolist()

        # For reproducibility
        random.seed(42)

        for i, source in enumerate(urls):
            outlinks = set()
            if outlink_counts[i] > 0:
                candidates = [u for u in urls if u != source]
                outlinks = random.sample(candidates, min(outlink_counts[i], len(candidates)))

            links[source] = outlinks
            all_pages.add(source)
            all_pages.update(outlinks)

            print(f"SOURCE: {source}")
            print(f"OUTLINKS (simulated): {outlinks}")

    return links, list(all_pages)

# Calculates PageRank using power iteration
def calculate_pagerank(links, pages, damping=0.85, max_steps=100, threshold=1e-6):
    total_pages = len(pages)

    if total_pages == 0:
        print("Error: No pages found. Check your input files or parsing logic.")
        return {}

    page_to_index = {page: i for i, page in enumerate(pages)}
    index_to_page = {i: page for i, page in enumerate(pages)}

    matrix = np.zeros((total_pages, total_pages))

    for source, outlinks in links.items():
        if source not in page_to_index:
            continue
        source_index = page_to_index[source]
        if not outlinks:
            matrix[:, source_index] = 1.0 / total_pages
        else:
            prob = 1.0 / len(outlinks)
            for target in outlinks:
                if target in page_to_index:
                    target_index = page_to_index[target]
                    matrix[target_index][source_index] = prob

    ranks = np.ones(total_pages) / total_pages

    for step in range(max_steps):
        new_ranks = (1 - damping) / total_pages + damping * matrix.dot(ranks)
        change = np.linalg.norm(new_ranks - ranks, 1)
        if change < threshold:
            break
        ranks = new_ranks

    pagerank_scores = {index_to_page[i]: ranks[i] for i in range(total_pages)}
    return pagerank_scores

# Get top 100 pages by PageRank
def get_top_100_pages(pagerank_scores):
    return sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:100]

# Main
def main():
    report_files = ["report_project2_crawl_en.csv"]

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

    output_file = "pagerank_output.csv"
    pd.DataFrame(top_pages, columns=["URL", "PageRank"]).to_csv(output_file, index=False)
    print(f"\nSaved PageRank results to: {output_file}")

if __name__ == "__main__":
    main()
