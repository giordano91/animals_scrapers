import datetime

from bs4 import BeautifulSoup

from scrapers.common.common_scrapers import BaseScraper
from scrapers.common.exceptions import RequestFailed
from scrapers.common.constants import ITALIAN_MONTHS


class SubitoItScraper(BaseScraper):

    SOURCE_NAME = "subito_it"

    def scrape(self):
        print(f"Starting to scrape...")
        # set this variable to True in order to keep track of the first request.
        # if the first request returns data, we will clean all the old data, otherwise not
        is_first_request = True
        # process all urls and for each of them scrape data from list page and also detail page
        for url in self.urls_list:
            # loop on all pages
            while True:
                url_with_page = url.format(self.page_number)

                try:
                    list_page = self.requests_manager.do_request(url_with_page)
                except RequestFailed:
                    break

                soup_list_page = BeautifulSoup(list_page.content, "html.parser")
                posts_list = soup_list_page.find_all("div", class_="items__item item-card item-card--small")
                print(f"Page #{self.page_number} - found {len(posts_list)} elements - {url_with_page}")

                # interrupt if there are no posts (last page reached)
                if len(posts_list) == 0:
                    break

                # since we don't want to loose data, clean old records only during the first request
                # and if it returns something
                if is_first_request is True:
                    self.db_manager.delete_records(self.SOURCE_NAME)
                    is_first_request = False

                for post in posts_list:
                    post_link = post.find("a", href=True).attrs["href"]

                    try:
                        post_detail = self.requests_manager.do_request(post_link)
                    except RequestFailed:
                        print("Impossible to retrieve information on post")
                        continue

                    soup_detail_page = BeautifulSoup(post_detail.content, "html.parser")

                    post_title = soup_detail_page.find("h1", class_="AdInfo_ad-info__title__7jXnY")
                    if post_title:
                        post_title = post_title.text
                    else:
                        print("Skipping post because mandatory attributes are null")
                        continue

                    post_date = soup_detail_page.find("span", class_="index-module_insertion-date__MU4AZ")
                    if post_date:
                        post_date = post_date.text.lower()
                        if "oggi" in post_date:
                            hour_minutes = post_date.split(" ")[-1]
                            hour_minutes_split = hour_minutes.split(":")
                            hour = hour_minutes_split[0]
                            minutes = hour_minutes_split[1]
                            today = datetime.datetime.today()
                            post_date = today.replace(hour=int(hour), minute=int(minutes),
                                                      second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
                        elif "ieri" in post_date:
                            hour_minutes = post_date.split(" ")[-1]
                            hour_minutes_split = hour_minutes.split(":")
                            hour = hour_minutes_split[0]
                            minutes = hour_minutes_split[1]
                            today = datetime.datetime.today()
                            post_date = today.replace(day=today.day-1,
                                                      hour=int(hour), minute=int(minutes),
                                                      second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            date_split = post_date.split(" ")
                            day = date_split[0]
                            month = ITALIAN_MONTHS.get(date_split[1])
                            hour_minutes_split = date_split[3].split(":")
                            hour = hour_minutes_split[0]
                            minutes = hour_minutes_split[1]
                            today = datetime.datetime.today()
                            post_date = today.replace(day=int(day), month=int(month),
                                                      hour=int(hour), minute=int(minutes),
                                                      second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

                    post_place = soup_detail_page.find("span", class_="AdInfo_ad-info__location__text__ZBFdn")
                    if post_place:
                        post_place = post_place.text

                    post_category = soup_detail_page.find("span", class_="feature-list_value__pgiul")
                    if post_category:
                        post_category = post_category.text

                    post_description = soup_detail_page.find("p", class_="AdDescription_description__gUbvH")
                    if post_description:
                        post_description = post_description.text

                    price = soup_detail_page.find("p", class_="index-module_price__N7M2x")
                    if price:
                        price = price.text

                    post_id = soup_detail_page.find("span", class_="AdInfo_ad-info__id__g3sz1")
                    if post_id:
                        post_id = post_id.text
                        post_id = post_id.replace("ID:", "").strip()

                    link_image = soup_detail_page.find("img", class_="Carousel_image__3muz6")
                    if link_image:
                        link_image = link_image.get("src")

                    self.results.append((post_title, post_date, post_place, post_category, post_description, price,
                                         post_id, post_link, link_image, self.SOURCE_NAME))

                self.page_number += 1

                if self.page_number % 20 == 0:
                    self.db_manager.insert_data(rows_list=self.results)
                    self.results = []
