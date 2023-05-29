import schedule
import time

from scrapers.common.exceptions import DbConnectionError
from my_pet_24_scraper import MyPet24Scraper


urls_list = [
    "https://mypet24.it/tutti-gli-annunci/?af_page={}&aff-cpt=1&category=181&razza&level&location&latitude&longitude"
]

retries = [2, 5, 10, 15]
for time_to_sleep in retries:
    try:
        scraper = MyPet24Scraper(urls_list)
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

