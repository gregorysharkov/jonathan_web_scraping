from pathlib import Path

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest

from ..settings import USER_AGENT


class ToreSaysSpider(CrawlSpider):
    name = "toresays"
    allowed_domains = ["toresaid.com"]
    start_urls = ["https://toresaid.com/episodeList.cshtml"]

    rules = (Rule(LinkExtractor(allow="api/episode/printtranscript")),)

    def start_requests(self):
        url = self.start_urls[0]
        self.log(f"Going for page {url}")
        # headers = (
        #     {
        #         "user_agent": USER_AGENT,
        #     },
        # )
        # , "headers": headers
        request = SplashRequest(
            url=url,
            callback=self.parse_item,
            args={"wait": 5},
            meta={
                "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G990F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36"
            },
        )
        yield request

    def parse(self, response):
        # super().parse(response)
        self.log(f"{response.headers=}")
        self.log(f"{response.status=}")

    def parse_item(self, response):
        self.log(f"************parsing item {response.url}")
