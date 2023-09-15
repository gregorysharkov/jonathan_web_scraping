from .episode_scraper import EpisodeScraper
from ..items import EpisodeItem


class StereoScraper(EpisodeScraper):
    name = "stereo"
    start_urls = [
        "https://toresaid.com/StereoList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            "tore/data/metadata/stereo.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
    }
