from .episode_scraper import EpisodeScraper
from ..items import EpisodeItem


class MiscellaneousScraper(EpisodeScraper):
    name = "miscellaneous"
    start_urls = [
        "https://toresaid.com/miscList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            "tore/data/metadata/miscellaneous.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
    }
