from pathlib import Path

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

from ..items import EpisodeItem

EPISODES_NAME = "episodes"
ALLOWED_DOMAINS = ["toresaid.com"]


class EpisodeScraper(scrapy.Spider):
    name = EPISODES_NAME
    allowed_domains = ALLOWED_DOMAINS
    start_urls = [
        "https://toresaid.com/episodeList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            f"tore/data/metadata/{EPISODES_NAME}.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
        "FILES_STORE": f"tore/data/{EPISODES_NAME}",
    }

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.log(f"{self.custom_settings=}")

    def start_requests(self):
        url = self.start_urls[0]
        request = SplashRequest(
            url=url,
            callback=self.parse,
            args={"wait": 2},
        )
        yield request

    def parse(self, response):
        """get list of episodes to be parsed and parse each one"""
        episode_list = response.xpath("//div[contains(@class, 'u-list-item')]")[:3]

        for episode_container in episode_list:
            episode = self.parse_episode(episode_container)
            self.log(f"{episode}")

            yield episode

    def parse_episode(self, episode_container):
        """parse single item in the article list"""

        itl = ItemLoader(
            item=EpisodeItem(),
            response=episode_container,
            selector=episode_container.xpath("."),
        )

        itl.add_xpath("title", ".//h4")
        itl.add_xpath("summary", ".//p/text()")
        itl.add_xpath(
            field_name="url",
            xpath=".//a[contains(@href, 'api/episode/printtranscript')]/@href",
        )
        itl.add_value("document_type", "pdf")
        itl.add_value("source", "https://toresaid.com")
        itl.add_value("meta_name", self.name)

        episode = itl.load_item()
        return episode
