# email-scraper

A general-purpose email scrapper with multithread capabilities that crawles domains to extract email addresses from the domain's websites.

## How to Use

The email scrapper is a two-step procedure:

1. Extract all links:

    ```bash
    python scrap_links.py [-h] [-m MAX_URLS] url
    ```

    where:

    * `url`: The URL to extract links from
    * `-m MAX_URLS`: Number of max URLs to crawl, default is `30`

2. Extract all e-mail addresses from the links:

    ```bash
    python scrap_email_threading.py [-h] [-t THREADS] file
    ```

    where:

    * `file`: File `.txt` containing url's to scrape.
    * `-t THREADS`: number of threads, default is `2`

## Example

Prefer `http://` over `https://`:

```bash
python scrap_links.py -m 100 "http://example.net"
python scrap_email_threading.py -t 4 example.net_internal_links.txt
```

## Creating a conda environment

In the root folder of the repository run:

```bash
conda env create --file environment.yml
```

## Notes

1.  RegEx to clean url

    ```
    http[s]?:\/\/(?:[w]{3}\.)?(.*)(?<!\/)
    ```

2. RegEx for Email

    ```
    (?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
    ```
