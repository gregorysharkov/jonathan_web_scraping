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

            # if not Path(episode["file"]).exists():
            #     yield Request(
            #         url=episode["episode_url"],
            #         callback=self.download_episode,
            #         cb_kwargs={"title": episode["title"]},
            #     )
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
        # # TODO: move to item pipeline
        # episode["file_name"] = str(self._get_filepath(relative=False))
        # episode["episode_date"] = self._get_episode_date(episode["title"])
        # episode["file_urls"] = [self._get_episode_url(episode)]
        return episode

    # def download_episode(self, response, title: str):
    #     """
    #     save the file from from the response to the specific location
    #     """

    #     path = self._get_filepath(title, relative=False)
    #     self.pdf_store_path.mkdir(parents=True, exist_ok=True)
    #     with open(path, "wb") as file:
    #         file.write(response.body)

    @property
    def _output_path(self):
        return Path() / "tore" / "data"

    @property
    def pdf_store_path(self):
        return self._output_path / self.name

    @staticmethod
    def _get_episode_date(title: str) -> str:
        """gets episode date from the title"""

        return title.split("_-_")[0]

    # def _get_filepath(self, title: str, relative=False) -> Path:
    def _get_filepath(self, relative=False) -> Path:
        """
        returns the pdf file path

        Args:
            title: title of the episode
            relative: boolean flag whether return a relative path

        Returns a path object
        """
        if relative:
            return Path("data/") / self.name

        return self.pdf_store_path

    def _get_episode_url(self, episode) -> str:
        """returns episode url for a given episode"""

        return "/".join(self.start_urls[0].split("/")[:-1]) + episode["url"]
