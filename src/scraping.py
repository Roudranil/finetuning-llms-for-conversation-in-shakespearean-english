import logging
from urllib.parse import urljoin
import os
import json

import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from tqdm import tqdm


CRAWLER_NAME = "shakespeare"
START_URLS = ["https://www.litcharts.com/shakescleare/shakespeare-translations"]
BASE_URL = "https://www.litcharts.com"
DATA_DIR = "../raw-data"


class ShakespeareSpider(scrapy.Spider):
    name = CRAWLER_NAME
    start_urls = START_URLS
    custom_settings = {"LOG_LEVEL": logging.WARNING}

    def parse(self, response: Response, **kwargs):
        base_url = BASE_URL
        next_pages = response.css("a.translation.hoverable::attr(href)").extract()
        print(f"==> LOADING BOOKS\n    NUM BOOKS = {len(next_pages)}")
        loop = tqdm(
            next_pages,
            position=0,
            leave=True,
            bar_format="{desc:<50}{percentage:3.0f}%|{bar:20}{r_bar}",
        )
        for relative_url in loop:
            url = urljoin(base_url, relative_url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_book_url,
                cb_kwargs={"book_name": relative_url.split("/")[-1]},
            )

    def parse_book_url(self, response: Response, book_name: str):
        base_url = BASE_URL
        next_pages = response.css("div.table-of-contents a::attr(href)").extract()
        if len(next_pages) == 0:
            return
        loop = tqdm(
            next_pages,
            position=1,
            leave=True,
            desc=f"==> Book {book_name}",
            bar_format="{desc:<50}{percentage:3.0f}%|{bar:20}{r_bar}",
        )
        for relative_url in loop:
            url = urljoin(base_url, relative_url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_chapters,
                cb_kwargs={
                    "book_name": book_name,
                    "chapter_name": relative_url.split("/")[-1],
                },
            )

    def parse_chapters(
        self,
        response: Response,
        book_name: str | None = None,
        chapter_name: str | None = None,
    ):
        dialogs = {"dialogs": []}
        text_matches = response.css(".comparison-row").getall()
        for i, matches in enumerate(text_matches[2:-1]):
            original_content_html = (
                Selector(text=matches).css(".original-content .speaker-text").get()
            )
            translated_content_html = (
                Selector(text=matches).css(".translation-content .speaker-text").get()
            )
            try:
                original_content_text = "".join(
                    Selector(text=original_content_html)
                    .css(".speaker-text ::text")
                    .getall()
                )
                translated_content_text = "".join(
                    Selector(text=translated_content_html)
                    .css(".speaker-text ::text")
                    .getall()
                )
            except:
                continue
            dialogs["dialogs"].append(
                {
                    "original": "".join(
                        filter(
                            lambda c: 0 <= ord(c) and ord(c) <= 255,
                            original_content_text,
                        )
                    ),
                    "translated": "".join(
                        filter(
                            lambda c: 0 <= ord(c) and ord(c) <= 255,
                            translated_content_text,
                        )
                    ),
                }
            )
        _save_dialogs(dialogs, book_name, chapter_name)


def _save_dialogs(dialogs, book_name, chapter_name):
    output_dir = os.path.join(DATA_DIR, book_name)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{chapter_name}.json"), "w") as f:
        json.dump(dialogs, f, indent=4)


process = CrawlerProcess()
process.crawl(ShakespeareSpider)
process.start()
