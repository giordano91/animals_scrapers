import time

from subito_it_scraper import SubitoItScraper


urls_list = [
    "https://www.subito.it/annunci-italia/vendita/animali/?q=cucciolata&o={}"
]

retries = [2, 5, 10, 15]
for time_to_sleep in retries:
    try:
        scraper = SubitoItScraper(urls_list)
    except Exception:
        print(f"mysql_db service is not up and running yet. Wait '{time_to_sleep}' seconds and try again")
        time.sleep(time_to_sleep)
    else:
        break
else:
    raise ConnectionRefusedError

print(f"Starting to scrape...")
scraper.scrape()
