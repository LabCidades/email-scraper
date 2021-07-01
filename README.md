# email-scraper

A general-purpose email scrapper written in Python that crawles websites to extract email addresses.

This repo is heavily based on [`apetz/email-scraper`](https://github.com/apetz/email-scraper) implementation.

## Overview

Uses [`scrapy`](https://scrapy.org). The project consists  of a single spider `EmailSpider` which takes a full domain `string` as an argument and begins crawling there. Two optional arguments add further tuning capability:
* `subdomain_exclusions` - optional `list` of subdomains to exclude from the crawl
* `crawl_js` - optional `boolean` [default=False], whether or not to follow links to javascript files and also search them for urls

The `crawl_js` parameter is needed only when a "perfect storm" of conditions exist:

1. there is no `sitemap.xml` available

2. there are clickable menu items that are **not** contained in `<a>` tags

3. those menu items execute javascript code that loads pages but the urls are in the .js file itself

Normally such links would not be followed and scraped for further urls, however if a single-page AngularJS-based site with no sitemap is crawled, and the menu links are in `<span>` elements, the pages will not be discovered unless the ng-app is crawled as well to extract the destinations of the menu items.

A possible workaround to parsing the js files would be to use Selenium Web Driver to automate the crawl. I decided against this because Selenium needs to know how to find the menu using CSS selector, class name, etc. and these are specific to the site itself. A Selenium-based solution would not be as general-purpose, but for an AngularJS-based menu, something like the following would work in Selenium:

```python
from selenium import webdriver
driver = webdriver.Firefox()
driver.get("http://angularjs-site.com")
menuElement = driver.find_element_by_class_name("trigger")
menuElement.click()
driver.find_elements_by_xpath('//li')[3].click() # for example, click the third item off the discovered menu list
```

For this solution I opted to design the crawler ***without*** Selenium, which means occasionally crawling JS files to root out further links.

## Implemented classes:
* `EmailSpider`: the spider itself
* `DeDupePipeline`: simple de-duplicator so that email addresses are only printed out once even if they are discovered multiple times
* `SubdomainBlockerMiddleware`: blocks subdomains in case crawl needs to exclude them
* `EmailAddressItem`: holds the email addresses as `scrapy.Items`. Allows the `scrapy` framework to output items into a number of
convenient formats (`CSV`, `JSON`, etc.)

## How to Run

For a each of single domain you can use the standard `scrapy` commands:
 ```bash
 # CSV
 scrapy crawl spider -a domain="your.domain.name" -o emails-found.csv

 # JSON
 scrapy crawl spider -a domain="your.domain.name" -o emails-found.json
 ```

Or with optional command line arguments like:

```bash
# CSV
scrapy crawl spider -a domain="your.domain.name" -a subdomain_exclusions="['blog', 'technology']" -a crawl_js=True -o emails-found.csv

# JSON
scrapy crawl spider -a domain="your.domain.name" -a subdomain_exclusions="['blog', 'technology']" -a crawl_js=True -o emails-found.json
```

## RegEx to clean url

```
http[s]?:\/\/(?:[w]{3}\.)?(.*)(?<!\/)
```
