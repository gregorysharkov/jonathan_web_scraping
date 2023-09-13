from pathlib import Path

import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(
                url=url,
                callback=self.parse,
                args={
                    "wait": 0.5,
                },
                endpoint="render.html",
            )

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
