from bs4 import BeautifulSoup

from scrapers.common.db_manager import DbManager
from scrapers.common.exceptions import RequestFailed
from scrapers.common.requests_manager import RequestsManager


class SubitoItScraper:

    TABLE_NAME = "subito_it"

    def __init__(self, urls_list):
        self.urls_list = urls_list
        self.page_number = 1
        self.results = []

        # init objects
        self.requests_manager = RequestsManager()
        self.db_manager = DbManager()

    def scrape(self):
        # process all urls and for each of them scrape data from list page and also detail page
        for url in self.urls_list:
            # loop on all pages
            while True:
                url = url.format(self.page_number)

                try:
                    list_page = self.requests_manager.do_request(url)
                except RequestFailed:
                    break

                soup_list_page = BeautifulSoup(list_page.content, "html.parser")
                posts_list = soup_list_page.find_all("div", class_="items__item item-card item-card--small")
                print("Page #{} - found {} elements".format(self.page_number, len(posts_list)))

                if len(posts_list) == 0:
                    # work finished!
                    break

                for post in posts_list:
                    post_link = post.find("a", href=True).attrs["href"]

                    try:
                        post_detail = self.requests_manager.do_request(post_link)
                    except RequestFailed:
                        print("Impossible to retrieve information on post")
                        continue

                    soup_detail_page = BeautifulSoup(post_detail.content, "html.parser")

                    post_title = soup_detail_page.find("h1", class_="AdInfo_ad-info__title__7jXnY").text
                    post_date = soup_detail_page.find("span", class_="index-module_insertion-date__MU4AZ").text
                    post_place = soup_detail_page.find("span", class_="AdInfo_ad-info__location__text__ZBFdn").text
                    post_category = soup_detail_page.find("span", class_="feature-list_value__pgiul").text
                    post_description = soup_detail_page.find("p", class_="AdDescription_description__gUbvH").text
                    post_id = soup_detail_page.find("span", class_="AdInfo_ad-info__id__g3sz1").text
                    link_image = soup_detail_page.find("img", class_="Carousel_image__3muz6")["src"]

                    self.results.append((post_title, post_date, post_place, post_category, post_description, post_id,
                                         post_link, link_image))

                self.page_number += 1

                if self.page_number % 20 == 0:
                    self.db_manager.insert_data(table_name=self.TABLE_NAME, rows_list=self.results)
                    self.results = []

