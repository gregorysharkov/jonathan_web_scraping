from pathlib import Path

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

from ..items import EpisodeItem


class EpisodeScraper(scrapy.Spider):
    name = "episodes"
    allowed_domains = ["toresaid.com"]
    start_urls = [
        "https://toresaid.com/episodeList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            "tore/data/metadata/episodes.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
    }

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.custom_settings = {
            "FEEDS": {
                self.metadata_store_path: {
                    "format": "json",
                },
            },
        }

        self.log(f"{self.custom_settings=}")

    def start_requests(self):
        url = self.start_urls[0]
        self.log(f"Going for page {url}")
        request = SplashRequest(
            url=url,
            callback=self.parse,
            args={"wait": 2},
        )
        yield request

    def parse(self, response):
        """get list of episodes to be parsed and parse each one"""
        episode_list = response.xpath("//div[contains(@class, 'u-list-item')]")[:3]

        for idx, episode_container in enumerate(episode_list):
            episode = self.parse_episode(episode_container, idx)
            episode_url = "/".join(self.start_urls[0].split("/")[:-1]) + episode["url"]
            file_path = self._get_filepath(
                title=episode["title"],
                relative=False,
            )

            if not file_path.exists():
                yield Request(
                    url=episode_url,
                    callback=self.download_episode,
                    cb_kwargs={"title": episode["title"]},
                )

            yield episode

    def parse_episode(self, episode_container, idx: int):
        """parse single item in the article list"""

        itl = ItemLoader(
            item=EpisodeItem(),
            response=episode_container,
            selector=episode_container.xpath("."),
        )

        itl.add_xpath("title", ".//h4")
        itl.add_xpath("summary", ".//p/text()")
        itl.add_xpath(
            "url",
            ".//a[contains(@href, 'api/episode/printtranscript')]/@href",
        )

        episode = itl.load_item()

        return episode

    def download_episode(self, response, title: str):
        """
        save the file from from the response to the specific location
        """

        path = self._get_filepath(title, relative=False)
        self.pdf_store_path.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as file:
            file.write(response.body)

    @property
    def output_path(self):
        return Path() / "tore" / "data"

    @property
    def pdf_store_path(self):
        return self.output_path / self.name

    @property
    def metadata_store_path(self):
        return self.output_path / "metadata" / f"{self.name}.json"

    @staticmethod
    def get_filename(title: str) -> str:
        """gets the filename from a given title"""

        return f"{title[:20]}.pdf"

    def _get_filepath(self, title: str, relative=False) -> Path:
        """
        returns the pdf file path

        Args:
            title: title of the episode
            relative: boolean flag whether return a relative path

        Returns a path object
        """
        filename = self.get_filename(title)
        if relative:
            return Path("data/") / self.name / filename

        return self.pdf_store_path / filename
