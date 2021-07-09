# email-scraper

A general-purpose email scrapper with multithread capabilities that crawles domains to extract email addresses from the domain's websites.

## How to Use

The email scrapper is a two-step procedure:

1. Extract all links:

    ```bash
    python scrap_emails.py url
    ```

    where:

    * `url`: The URL to extract links from


2. Proccess all e-mail addresses from the file with e-mails:

    ```bash
    python clean_emails.py file
    ```

    where:

    * `file`: File `.txt` containing e-mai's to clean.

## Example

Prefer `https://` over `http://`:

```bash
python scrap_emails.py "https://example.net" or "https://www.example.net"
python clean_emails.py "www.example.net.txt"
```

You can use a `for`-loop in bash for massive scraping:

```bash
for i in $(cat domain_list.txt); do python scrap_emails.py "$i"; done

for i in $(ls *.txt); do python clean_emails.py $i; done
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
