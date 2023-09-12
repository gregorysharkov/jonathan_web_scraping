from pathlib import Path

import scrapy


class ToreSaysSpider(scrapy.Spider):
    name='toresays'

    def start_requests(self):
        urls = [
            "https://toresaid.com/episodeList.cshtml",
        ]

        for url in urls:
            self.log(f'Going for page {url}')
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log(f'{response}')
