from bs4 import BeautifulSoup

from scrapers.common.common_scrapers import BaseScraper
from scrapers.common.exceptions import RequestFailed


class AnnunciAnimaliScraper(BaseScraper):

    BASE_URL = "https://www.annuncianimali.it"
    SOURCE_NAME = "annunci_animali"

    def scrape(self):
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
                posts_list_div = soup_list_page.find("div", {"data-testid": "search-results"})
                posts_list = posts_list_div.find_all("a")
                print(f"Page #{self.page_number} - found {len(posts_list)} elements - {url_with_page}")

                # interrupt if there are no posts (last page reached)
                if len(posts_list) == 0:
                    break

                for post in posts_list:
                    post_link = post.attrs["href"]
                    post_link_url = f"{self.BASE_URL}{post_link}"

                    try:
                        post_detail = self.requests_manager.do_request(post_link_url)
                    except RequestFailed:
                        print("Impossible to retrieve information on post")
                        continue

                    soup_detail_page = BeautifulSoup(post_detail.content, "html.parser")

                    post_title = soup_detail_page.find("h1")
                    if post_title:
                        post_title = post_title.text
                    else:
                        print(f"Skipping post because title is null - {post_link_url}")
                        continue

                    post_id = None
                    ads_info_container = soup_detail_page.find("div",
                                                               {"data-component": "ListingDetailsSectionParameters"})
                    ads_info_div_list = ads_info_container.find_all("div", {"data-testid": "details-parameter"}) or []
                    for ads_info in ads_info_div_list:
                        span_list = ads_info.find_all("span")
                        if span_list and isinstance(span_list, list) is True:
                            if len(span_list) == 2:

                                # post_id
                                if span_list[0].text.lower() == "id annuncio":
                                    post_id = span_list[1].text
                                    break

                    if post_id is None:
                        print(f"Skipping post because post_id is null - {post_link_url}")
                        continue

                    post_date = None

                    post_place = soup_detail_page.find("a", {"data-testid": "detail-value-search"})
                    if post_place:
                        post_place = post_place.text

                    post_category = "Cani"

                    post_description_div = soup_detail_page.find("div", {"data-testid": "listing-description"})
                    post_description = post_description_div.find_all("span") if post_description_div else []
                    if len(post_description) == 2:
                        post_description = post_description[1].text
                    else:
                        post_description = None

                    price_div = soup_detail_page.find("div", {"data-component": "ListingDetailsSidebarPriceBox"})
                    price = price_div.find("span") if price_div else None
                    if price:
                        price = price.text

                    link_image = soup_detail_page.find("img", {"data-nimg": "future-fill"})
                    if link_image:
                        link_image = link_image.get("src")

                    self.results.append((post_title, post_date, post_place, post_category, post_description, price,
                                         post_id, post_link, link_image, self.SOURCE_NAME))

                self.page_number += 1

                if self.page_number % 10 == 0:
                    self.db_manager.replace_records(rows_list=self.results)
                    self.results = []

            self.page_number = 1
