import requests
import time

from scrapers.common.exceptions import RequestFailed


class RequestsManager:

    RETRIES = [0, 1, 5, 10, 20]
    TIMEOUT = 60

    def __init__(self):
        pass

    def do_request(self, url):
        for sleeping_time in self.RETRIES:
            time.sleep(sleeping_time)
            try:
                return requests.get(url, timeout=self.TIMEOUT)
            except Exception as e:
                print("An error occurred: {}".format(e))
                continue
        else:
            RequestFailed("All retries have been done and the error is still present. Aborting.")
