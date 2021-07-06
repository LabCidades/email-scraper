"""
Scraping email extractor using threads
"""

import re
import time
import urllib3
import certifi
import concurrent.futures

from bs4 import BeautifulSoup
from datetime import datetime

# setting SSL conection
http = urllib3.PoolManager(ca_certs=certifi.where())

# file results from scraping
date = datetime.today().strftime('%Y-%m-%d')
timestamp = datetime.timestamp(datetime.now())
file_out = f"scrap_result_{timestamp}_{date}.txt"

def download_email(url):
    """
    Scraping all URLs that is found in input file
    """
    soup = BeautifulSoup(http.request('GET', url).data.decode('utf-8'), "html.parser")
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', str(soup))
    emails = set(emails)
    for e in emails:
        with open(file_out, "a") as lnkfile:
            lnkfile.write(e + "\n")
        print(e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="E-mail extractor by scraping")
    parser.add_argument("-t", "--threads", help="Number of threads, default is 2.", default=2, type=int)
    parser.add_argument("file", help="File '.txt' containing url's.")

    args = parser.parse_args()

    # file containing url's
    f = open(args.file, "r")
    urls = f.read().splitlines()

    # number of threads
    threads = (args.threads if args.threads != None else 2)

    # run concurrence
    with concurrent.futures.ThreadPoolExecutor(threads) as executor:
        executor.map(download_email, urls)
