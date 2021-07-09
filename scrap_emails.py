"""
Scraping email extractor using threads
Version 1.1
"""
import re
import sys
import time
import logging
import urllib3
import certifi
import threading

from pathlib import Path
from setup import NO_PARSE
from pysitemap import crawler
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlsplit

# setting SSL conection
http = urllib3.PoolManager(ca_certs=certifi.where())

class FetchUrl(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.setDaemon = True
        self.url = url

    def run(self):
        urlHandler = urllib3.PoolManager(ca_certs=certifi.where())
        
        # Extract email's
        get_emails(self.url)

        finished_fetch_url(self.url)


def finished_fetch_url(url):
    global left_to_fetch
    left_to_fetch -= 1
    print("\tget email:", url)

def get_emails(url):
    soup = BeautifulSoup(http.request('GET', url).data.decode('utf-8'), "html.parser")
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', str(soup))
    emails = set(emails)
    for email in emails:
        with open(out, "a") as lnkfile:
            if not re.search(r"exemple.com|example.com|dominio.com.br|exemplo.com.br|email.com|suaempresaaqui.org.br|wixpress.com|wix.com", email):
                lnkfile.write(email + "\n")

if __name__ == '__main__':
    if '--iocp' in sys.argv:
        from asyncio import events, windows_events
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)

    root_url =  sys.argv[1]
    file = urlparse(root_url).netloc + '.xml'
    global out
    out = urlparse(root_url).netloc + '.txt'
   
    # Run threading crawler
    crawler(root_url, out_file=file, maxtasks=1000, exclude_urls=NO_PARSE)

    urls = set()
    
    # Read the XML file
    with open(file, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = BeautifulSoup(content, "lxml")

        result = bs_content.find_all("loc")

        for r in result:
            urls.add(r.get_text())
    
    left_to_fetch = len(urls)
    for url in urls:
        FetchUrl(url).start()
