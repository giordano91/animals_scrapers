import schedule
import time

from scrapers.common.exceptions import DbConnectionError
from annunci_animali_scraper import AnnunciAnimaliScraper


urls_list = [
    "https://www.annuncianimali.it/vendita/cani/locale/locale/pagina-{}/"
]

retries = [2, 5, 10, 15]
for time_to_sleep in retries:
    try:
        scraper = AnnunciAnimaliScraper(urls_list)
    except Exception:
        print(f"mysql_db service is not up and running yet. Wait '{time_to_sleep}' seconds and try again")
        time.sleep(time_to_sleep)
    else:
        break
else:
    raise DbConnectionError("Impossible to connect to the database, abort!")

# run the scraper and schedule it every 6 hours
scraper.scrape()
schedule.every(1).hours.do(scraper.scrape)

# apply all the pending schedules
while True:
    schedule.run_pending()
    time.sleep(1)

