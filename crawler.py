# crawls 3 seed urls each in a different domain and language, and seperates output into 3 folders. english, german, french
import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse, urljoin

# Function to check if a URL belongs to the desired domain
def is_valid_domain(url, allowed_domains):
    domain = urlparse(url).netloc
    return domain in allowed_domains

# Function to check if a page is in the desired language
def is_valid_language(soup, target_language):
    lang = soup.html.get("lang", "").lower()
    return lang == target_language

# Function to get outlinks from a page
def get_outlinks(soup, base_url):
    outlinks = set()
    for link in soup.find_all('a', href=True):
        url = urljoin(base_url, link['href'])
        if base_url in url:
            outlinks.add(url)
    return outlinks

# Main function to crawl the website using the seed url, specific language, max pages
def crawl(seed_urls, allowed_domains, target_language, crawl_name, max_pages=50):
    crawled_urls = set()
    to_crawl = seed_urls[:]
    report_data = []

    # Creates a new folder for this crawl to seperate each crawl's outputs
    repository_dir = f"repository_{crawl_name}"
    if not os.path.exists(repository_dir):
        os.makedirs(repository_dir)
        print(f"Created folder: {repository_dir}")

    while to_crawl and len(crawled_urls) < max_pages:
        url = to_crawl.pop(0)
        if url in crawled_urls:
            continue
        
        print(f"Crawling: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser") # html parsing
            
            if is_valid_language(soup, target_language):
                # Saves the html page content to the specific crawl folder
                file_name = os.path.join(repository_dir, f"{len(crawled_urls)+1}.html")
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f"Saved: {file_name}")
                
                # Counts the number of outlinks and adds to the report.csv file
                outlinks = get_outlinks(soup, url)
                report_data.append([url, len(outlinks)])

                # Add outlinks to the crawl queue
                to_crawl.extend(outlinks)

                crawled_urls.add(url)
            else:
                print(f"Skipped {url}, language mismatch.")
        
        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}") # if an error is encountered, print error message

    # Save the report CSV file with all 50 outlinks
    report_filename = f"report_{crawl_name}.csv"
    with open(report_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Outlinks Count"])
        writer.writerows(report_data)

    print(f"Crawling completed. {len(crawled_urls)} pages crawled.")
    print()
    return crawled_urls, report_data

# Testing the web crawler
if __name__ == "__main__":
    # Defining seed URLs for different languages
    seed_urls_en = ["https://www.cpp.edu"]
    seed_urls_zh = ["https://www.spiegel.de"]
    seed_urls_fr = ["https://www.lemonde.fr"]

    # Allowed domains
    allowed_domains = ["cpp.edu", "spiegel.com", "lemonde.fr"]
    
    # Crawl for the different languages
    for language, seed_urls in zip(["en", "de", "fr"], [seed_urls_en, seed_urls_zh, seed_urls_fr]):
        crawl_name = f"crawl_{language}"  # Create crawl_name dynamically to organize each crawl by domain and language (crawl_en, crawl_zh, crawl_fr)
        print(f"Starting crawl for {language}...")
        crawled_urls, report_data = crawl(seed_urls, allowed_domains, language, crawl_name)

