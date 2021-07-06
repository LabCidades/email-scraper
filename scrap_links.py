# https://github.com/x4nth055/pythoncode-tutorials/tree/master/web-scraping/link-extractor

import re
import urllib3
import certifi
import requests

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

http = urllib3.PoolManager(ca_certs=certifi.where())

# initialize the set of links (unique links)
internal_urls = set()

total_urls_visited = 0

def check_url(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except:
        pass


def get_links(url):
    try:
        urls = set()
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            
            if re.search("mp3|wav|mp4|avi|pdf|jpg|jpeg|png|gif|mailto|svg|mailto|doc|docx|ppt|pptx|css|img|xls|xlsx", href):
                continue
            
            if re.search("facebook|youtube|twitter|linkedin|instragram", href):
                continue

            if href == "" or href is None:
                continue

            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            if not check_url(href):
                continue

            if href in internal_urls:
                continue
            
            if domain_name not in href:
                continue
            print("\tLink found:", href)
            urls.add(href)
            internal_urls.add(href)
    except:
        pass
    return urls


def crawl(url, max_urls=1000):
    try:
        global total_urls_visited
        total_urls_visited += 1
        print("Crawling:", url)
        links = get_links(url)
        for link in links:
            if total_urls_visited > max_urls:
                break
            crawl(link, max_urls=max_urls)
    except:
        pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    crawl(url, max_urls=max_urls)

    print("\nTotal links extracted:", len(internal_urls))
    print("Total crawled URLs:", max_urls)

    domain_name = urlparse(url).netloc

    # save the internal links to a file
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)
