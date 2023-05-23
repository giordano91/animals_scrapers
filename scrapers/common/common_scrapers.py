from scrapers.common.db_manager import DbManager
from scrapers.common.requests_manager import RequestsManager


class BaseScraper:
    BASE_URL = None
    SOURCE_NAME = None

    def __init__(self, urls_list):
        self.urls_list = urls_list
        self.page_number = 1
        self.results = []

        # init objects
        self.requests_manager = RequestsManager()
        self.db_manager = DbManager()

    def scrape(self):
        raise NotImplementedError
