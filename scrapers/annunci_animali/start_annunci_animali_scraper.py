import os
import json
import schedule
import time

from scrapers.common.exceptions import DbConnectionError
from annunci_animali_scraper import AnnunciAnimaliScraper

URL_LIST = json.loads(os.environ["URL_LIST"])
DB_CONNECTION_RETRIES = json.loads(os.environ["DB_CONNECTION_RETRIES"])
SCHEDULE_HOURS = int(os.environ["SCHEDULE_HOURS"])


for time_to_sleep in DB_CONNECTION_RETRIES:
    try:
        scraper = AnnunciAnimaliScraper(URL_LIST)
    except Exception:
        print(f"mysql_db service is not up and running yet. Wait '{time_to_sleep}' seconds and try again")
        time.sleep(time_to_sleep)
    else:
        break
else:
    raise DbConnectionError("Impossible to connect to the database, abort!")

# run the scraper and schedule it every 6 hours
scraper.scrape()
schedule.every(SCHEDULE_HOURS).hours.do(scraper.scrape)

# apply all the pending schedules
while True:
    schedule.run_pending()
    time.sleep(1)

