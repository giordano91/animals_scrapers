import datetime
import json
import os
import unicodedata

from bs4 import BeautifulSoup

from scrapers.common.common_scrapers import BaseScraper
from scrapers.common.exceptions import RequestFailed


class MyPet24Scraper(BaseScraper):

    SOURCE_NAME = "my_pet_24"

    def scrape(self):
        num_pages_save_records = int(os.environ["NUM_PAGES_SAVE_RECORDS"])

        print(f"Starting to scrape...")
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
                posts_list = soup_list_page.find_all("div", class_="af-item-wrap")
                print(f"Page #{self.page_number} - found {len(posts_list)} elements - {url_with_page}")

                # interrupt if there are no posts (last page reached)
                if len(posts_list) == 0:
                    break

                for post in posts_list:
                    post_link = post.find("a", class_="advert-media", href=True).attrs["href"]

                    try:
                        post_detail = self.requests_manager.do_request(post_link)
                    except RequestFailed:
                        print("Impossible to retrieve information on post")
                        continue

                    soup_detail_page = BeautifulSoup(post_detail.content, "html.parser")

                    post_title = soup_detail_page.find("h1", class_="blog-item-title")
                    if post_title:
                        post_title = post_title.text
                        if len(post_title) > 255:
                            print("Title too long, skipping record")
                            continue
                    else:
                        print(f"Skipping post because title is null - {post_link}")
                        continue

                    post_id = None
                    post_place = None
                    post_date = None
                    info_post = soup_detail_page.find_all("ul", class_="single-meta")
                    if info_post and isinstance(info_post, list):
                        if len(info_post) == 1:
                            info_post = unicodedata.normalize("NFKD", info_post[0].text)
                            info_post_split = info_post.replace("\t", "").replace("\n", "").split("  ")
                            post_place = "{}{}".format(info_post_split[0].split(" ")[0].strip(),
                                                       info_post_split[0].split(" ")[1].strip())
                            post_id = info_post_split[1].strip()
                            post_date_str = info_post_split[2].strip()
                            post_date = datetime.datetime.strptime(post_date_str, '%d/%m/%Y')

                    if post_id is None:
                        print(f"Skipping post because post_id is null - {post_link}")
                        continue

                    puppy_birthdate = None

                    post_description = soup_detail_page.find("div", class_="post-content")
                    if post_description:
                        post_description = post_description.text

                    price = soup_detail_page.find("div", class_="price")
                    if price:
                        price = price.text

                    link_images = [img.get("src") for img in soup_detail_page.find_all("img", class_="attachment-full")]

                    breed_id = None
                    species_id = None

                    self.results.append((post_title, post_date, puppy_birthdate, post_place, post_description, price,
                                         post_id, post_link, json.dumps(link_images), self.SOURCE_NAME, breed_id,
                                         species_id))

                self.page_number += 1

                if self.page_number % num_pages_save_records == 0:
                    self.db_manager.replace_records(rows_list=self.results)
                    self.results = []

        self.page_number = 1
