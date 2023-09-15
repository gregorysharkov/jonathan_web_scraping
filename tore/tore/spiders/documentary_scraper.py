from .episode_scraper import EpisodeScraper
from ..items import EpisodeItem


class DocumentaryScraper(EpisodeScraper):
    name = "documentaries"
    start_urls = [
        "https://toresaid.com/DocumList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            "tore/data/metadata/documentaries.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
    }
