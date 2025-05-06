import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse, urljoin

# Check if a URL belongs to one of the allowed domains
def is_valid_domain(url, allowed_domains):
    domain = urlparse(url).netloc
    return any(domain.endswith(d) for d in allowed_domains)

# Check if a page is in the desired language
def is_valid_language(soup, target_language):
    if soup.html and soup.html.get("lang"):
        return soup.html.get("lang", "").lower() == target_language
    return False

# Extract and normalize outlinks that stay within allowed domains
def get_outlinks(soup, base_url, allowed_domains):
    outlinks = set()
    for a in soup.find_all('a', href=True):
        href = urljoin(base_url, a['href'])
        if is_valid_domain(href, allowed_domains):
            outlinks.add(href)
    return list(outlinks)

# Main crawl function, now recording actual outlink lists for PageRank
def crawl(seed_urls, allowed_domains, target_language, crawl_name, max_pages=500):
    crawled = set()
    queue = seed_urls[:]
    link_graph = {}

    folder = f"repository_project2.1_{crawl_name}"
    os.makedirs(folder, exist_ok=True)

    while queue and len(crawled) < max_pages:
        url = queue.pop(0)
        if url in crawled:
            continue
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            if is_valid_language(soup, target_language):
                # save raw HTML
                idx = len(crawled) + 1
                with open(os.path.join(folder, f"{idx}.html"), 'w', encoding='utf-8') as f:
                    f.write(resp.text)

                # collect outlinks for this URL
                outs = get_outlinks(soup, url, allowed_domains)
                link_graph[url] = outs

                # enqueue new URLs
                for tgt in outs:
                    if tgt not in crawled and tgt not in queue:
                        queue.append(tgt)

                crawled.add(url)
                print(f"Crawled #{idx}: {url} ({len(outs)} outlinks)")
            else:
                print(f"Skipped (lang mismatch): {url}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # write graph CSV for PageRank
    csv_file = f"report_project2.1_{crawl_name}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(["URL", "Outlinks"])
        for src, outs in link_graph.items():
            writer.writerow([src, str(outs)])

    print(f"Crawl complete: {len(crawled)} pages. Graph saved to {csv_file}.")
    return link_graph

# Example usage
if __name__ == "__main__":
    seeds_en = ["https://www.cpp.edu"]
    allowed = ["cpp.edu"]
    graph_en = crawl(seeds_en, allowed, 'en', 'crawl_en')
    # graph_en is now a dict of URL -> [list of outlink URLs]

